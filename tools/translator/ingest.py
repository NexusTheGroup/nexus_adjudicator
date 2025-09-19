#!/usr/bin/env python3
from __future__ import annotations

import glob
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
    from zoneinfo import ZoneInfoNotFoundError
except ImportError:  # pragma: no cover
    ZoneInfo = None
    ZoneInfoNotFoundError = Exception

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parents[2]
TRANSLATOR_DIR = Path(__file__).resolve().parent
ADAPTER_PATH = TRANSLATOR_DIR / "adapter.yml"
DIAGRAM_SCRIPT = ROOT / "tools" / "diagrams" / "remediate.py"
ACTION_LEDGER = ROOT / ".artifacts" / "action_ledger.jsonl"
CHECKIN_FILE = ROOT / "AGENTS.md"

LIST_FIELDS = {"actors", "acceptance_criteria", "non_goals", "dependencies", "risks"}
CHECKIN_TZ = "America/Chicago"


def load_adapter() -> dict:
    data = ADAPTER_PATH.read_text(encoding="utf-8")
    if not yaml:
        return simple_yaml_load(data)
    return yaml.safe_load(data)


def simple_yaml_load(data: str) -> dict:
    result: dict[str, dict[str, str] | str] = {}
    current_section: dict[str, str] | None = None
    for raw in data.splitlines():
        line = raw.rstrip()
        if not line or line.strip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        key, sep, value = line.strip().partition(":")
        if not sep:
            continue
        value = value.strip().strip('"')
        if indent == 0 and not value:
            current_section = {}
            result[key] = current_section
            continue
        target = current_section if indent > 0 and current_section is not None else result
        target[key] = value
        if indent == 0:
            current_section = None
    return result


def find_latest_spec_kit(cfg: dict) -> tuple[str, Path, Path, Path]:
    spec_glob = cfg["spec_kit"]["spec_glob"]
    plan_glob = cfg["spec_kit"]["plan_glob"]
    tasks_glob = cfg["spec_kit"]["tasks_glob"]

    reqs = glob.glob(spec_glob, recursive=True)
    plans = glob.glob(plan_glob, recursive=True)
    tasks = glob.glob(tasks_glob, recursive=True)
    if not reqs or not plans or not tasks:
        raise FileNotFoundError("Spec-Kit incomplete: requirement/plan/tasks not found")

    plan_index = index_by_slug(plans)
    task_index = index_by_slug(tasks)

    best = None
    for req in reqs:
        slug = slug_from_path(req)
        plan = plan_index.get(slug)
        task = task_index.get(slug)
        if not plan or not task:
            continue
        mtime = max(os.path.getmtime(req), os.path.getmtime(plan), os.path.getmtime(task))
        if not best or mtime > best[0]:
            best = (mtime, slug, Path(req), Path(plan), Path(task))
    if not best:
        raise FileNotFoundError("No matching Spec-Kit triplet located")
    return best[1:]  # slug, req, plan, task


def index_by_slug(paths: list[str]) -> dict[str, Path]:
    out: dict[str, Path] = {}
    for p in paths:
        slug = slug_from_path(p)
        if slug not in out:
            out[slug] = Path(p)
    return out


def slug_from_path(path: str | Path) -> str:
    p = Path(path)
    return sanitize_slug(p.parent.name or p.stem)


def sanitize_slug(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", text.strip().lower())
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug or "spec-kit"


def parse_markdown(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    frontmatter = {}
    body_start = 0
    if lines and lines[0].strip() == "---":
        for idx in range(1, len(lines)):
            if lines[idx].strip() == "---":
                fm_text = "\n".join(lines[1:idx])
                frontmatter = load_yaml_fragment(fm_text)
                body_start = idx + 1
                break
    body_lines = lines[body_start:]
    section_text: dict[str, str] = {}
    bullet_map: dict[str, list[str]] = {}
    first_h1 = None
    current_key = None
    current_lines: list[str] = []

    def flush():
        nonlocal current_key, current_lines
        if current_key is None:
            return
        cleaned = normalize_section(current_lines)
        if cleaned:
            section_text[current_key] = cleaned
        current_lines = []

    for raw in body_lines:
        if raw.lstrip().startswith("#"):
            hashes = len(raw) - len(raw.lstrip("#"))
            heading = raw.strip("# ")
            if hashes == 1 and not first_h1:
                first_h1 = heading.strip()
            if hashes >= 1:
                flush()
                current_key = sanitize_slug(heading)
                bullet_map.setdefault(current_key, [])
            continue
        if current_key is None:
            continue
        stripped = raw.strip()
        if stripped.startswith("- ") or stripped.startswith("* "):
            bullet = stripped[2:].strip()
            if bullet:
                bullet_map.setdefault(current_key, []).append(bullet)
        current_lines.append(raw)
    flush()

    return {
        "frontmatter": frontmatter or {},
        "h1": first_h1 or path.stem,
        "section": section_text,
        "bullets": bullet_map,
    }


def load_yaml_fragment(text: str) -> dict:
    if not text.strip():
        return {}
    if yaml:
        data = yaml.safe_load(text)
        return data or {}
    return simple_yaml_load(text)


def normalize_section(lines: list[str]) -> str:
    cleaned: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("- ") or stripped.startswith("* "):
            cleaned.append(stripped[2:].strip())
        else:
            cleaned.append(stripped)
    return "\n".join(cleaned).strip()


def evaluate_mapping(expr: str, ctx: dict) -> str | list[str] | None:
    for part in expr.split("||"):
        key = part.strip()
        if not key:
            continue
        value = resolve_path(key, ctx)
        if value is None:
            continue
        if isinstance(value, str) and not value.strip():
            continue
        if isinstance(value, list) and not any(str(v).strip() for v in value):
            continue
        return value
    return None


def resolve_path(path: str, ctx: dict):
    parts = path.split(".")
    current = ctx
    for segment in parts:
        segment = segment.strip()
        if not segment:
            return None
        if isinstance(current, dict):
            current = current.get(segment)
        else:
            return None
        if current is None:
            return None
    return current


def coerce_field(name: str, value) -> str | list[str]:
    if name in LIST_FIELDS:
        if value is None:
            return []
        if isinstance(value, list):
            return [v.strip() for v in value if str(v).strip()]
        if isinstance(value, str):
            items = re.split(r"[\n,;+]", value)
            return [item.strip() for item in items if item.strip()]
        return [str(value).strip()]
    if value is None:
        return ""
    if isinstance(value, list):
        return "\n".join(str(v).strip() for v in value if str(v).strip())
    return str(value).strip()


def build_contract(mapping: dict[str, str], spec_ctx: dict, slug: str, req: Path, plan: Path, tasks: Path) -> dict:
    contract_fields = {}
    context = {
        "frontmatter": spec_ctx.get("frontmatter", {}),
        "h1": spec_ctx.get("h1"),
        "section": spec_ctx.get("section", {}),
        "bullets": spec_ctx.get("bullets", {}),
    }
    for key, expr in mapping.items():
        value = evaluate_mapping(expr, context)
        contract_fields[key] = coerce_field(key, value)
    generated = datetime.now(timezone.utc).isoformat()
    return {
        "product": contract_fields,
        "source": {
            "requirement": str(req),
            "plan": str(plan),
            "tasks": str(tasks),
        },
        "metadata": {
            "adapter": str(ADAPTER_PATH),
            "generated_at": generated,
            "slug": slug,
        },
    }


def ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, payload: dict) -> None:
    ensure_dir(path)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def extract_table_items(ctx: dict, candidates: list[str]) -> list[str]:
    for key in candidates:
        from_bullets = ctx.get("bullets", {}).get(key)
        items = to_list(from_bullets)
        if items:
            return items
        from_section = ctx.get("section", {}).get(key)
        items = to_list(from_section)
        if items:
            return items
    return []


def to_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    if isinstance(value, str):
        parts = re.split(r"[\n\r,;+]", value)
        return [p.strip() for p in parts if p.strip()]
    return [str(value).strip()]


def split_item(text: str) -> tuple[str, str]:
    if ":" in text:
        name, detail = text.split(":", 1)
        return name.strip(), detail.strip()
    if " - " in text:
        name, detail = text.split(" - ", 1)
        return name.strip(), detail.strip()
    return text.strip(), ""


def escape_table_cell(text: str) -> str:
    return str(text or "").replace("|", "\\|").replace("\n", " ")


def build_table(rows: list[tuple[str, str]], headers: tuple[str, str]) -> str:
    lines = [
        f"| {headers[0]} | {headers[1]} |",
        "| --- | --- |",
    ]
    if not rows:
        rows = [("TBD", "Provide details")]
    for left, right in rows:
        lines.append(
            f"| {escape_table_cell(left or 'TBD')} | {escape_table_cell(right or '')} |"
        )
    return "\n".join(lines)


def build_work_order(path: Path, title: str, slug: str, spec_ctx: dict, plan_ctx: dict, tasks_ctx: dict) -> None:
    ensure_dir(path)
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    interfaces = extract_table_items(plan_ctx, ["interfaces", "integration_points", "apis", "services"])
    environments = extract_table_items(plan_ctx, ["environments", "env", "deployments", "infrastructure"])
    tests = extract_table_items(tasks_ctx, ["tests", "testing", "verification", "qa", "tasks"])

    interface_rows = [split_item(item) for item in interfaces]
    environment_rows = [split_item(item) for item in environments]
    test_rows = [split_item(item) for item in tests]

    lines = [
        f"# Work Order — {title}",
        "",
        f"_Generated {generated} from `{slug}` Spec-Kit._",
        "",
        "## Interfaces",
        build_table(interface_rows, ("Interface", "Notes")),
        "",
        "## Environments",
        build_table(environment_rows, ("Environment", "Details")),
        "",
        "## Tests",
        build_table(test_rows, ("Test", "Coverage / Target")),
    ]

    summary = spec_ctx.get("section", {}).get("summary")
    if summary:
        lines.extend(["", "## Summary", summary])

    path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def build_diagram(paths: dict, title: str, summary: str, slug: str) -> tuple[Path, Path]:
    diagrams_dir = Path(paths["diagrams_dir"])
    mmd_path = ROOT / diagrams_dir / f"{slug}.mmd"
    ensure_dir(mmd_path)
    label_title = title.replace("\"", "'")
    label_summary = (summary or "").replace("\"", "'")[:120]
    if label_summary:
        summary_node = f"    R --> S[\"Summary: {label_summary}\"]"
    else:
        summary_node = ""
    mmd = "\n".join([
        "flowchart TD",
        f"    R[\"Requirement: {label_title}\"]",
        "    P[\"Plan\"]",
        "    T[\"Tasks\"]",
        "    R --> P",
        "    P --> T",
        summary_node,
    ]).strip() + "\n"
    mmd_path.write_text(mmd, encoding="utf-8")
    html_path = mmd_path.with_suffix(".html")
    subprocess.run([sys.executable, str(DIAGRAM_SCRIPT), str(mmd_path), str(html_path)], check=False)
    return mmd_path, html_path


def append_action_ledger(slug: str, contract_path: Path, work_order_path: Path, mmd_path: Path, html_path: Path) -> None:
    ACTION_LEDGER.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "slug": slug,
        "artifacts": {
            "contract": str(contract_path),
            "work_order": str(work_order_path),
            "diagram_mmd": str(mmd_path),
            "diagram_html": str(html_path),
        },
    }
    with ACTION_LEDGER.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")


def append_checkin(slug: str) -> None:
    tz = timezone.utc
    if ZoneInfo:
        try:
            tz = ZoneInfo(CHECKIN_TZ)
        except ZoneInfoNotFoundError:  # pragma: no cover
            tz = timezone.utc
    now = datetime.now(tz).replace(microsecond=0)
    login = now.isoformat()
    row = f"| Codex | GPT-5 | sess-{now.strftime('%Y%m%d%H%M%S')} | {login} | spec-translation | {slug} |  | Translated {slug} Spec-Kit | - |"
    content = CHECKIN_FILE.read_text(encoding="utf-8")
    lines = content.splitlines()
    insert_at = None
    for idx, line in enumerate(lines):
        if "<!-- >>ROW:CHECKIN:END -->" in line:
            insert_at = idx
            break
    if insert_at is None:
        raise RuntimeError("CHECKIN markers missing in AGENTS.md")
    lines.insert(insert_at, row)
    CHECKIN_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    adapter = load_adapter()
    try:
        slug, req, plan, tasks = find_latest_spec_kit(adapter)
    except FileNotFoundError as err:
        print(f"No Spec-Kit located: {err}")
        return
    spec_ctx = parse_markdown(req)
    plan_ctx = parse_markdown(plan)
    tasks_ctx = parse_markdown(tasks)

    contract = build_contract(adapter.get("mapping", {}), spec_ctx, slug, req, plan, tasks)
    contract_path = ROOT / "artifacts" / "contracts" / "Product_Contract.json"
    write_json(contract_path, contract)

    work_order_path = ROOT / adapter["links"]["work_order_path"]
    build_work_order(work_order_path, contract["product"].get("title", ""), slug, spec_ctx, plan_ctx, tasks_ctx)

    summary_value = contract["product"].get("summary", "")
    diagrams = build_diagram(adapter["links"], contract["product"].get("title", slug), summary_value if isinstance(summary_value, str) else "", slug)

    append_action_ledger(slug, contract_path, work_order_path, diagrams[0], diagrams[1])
    append_checkin(slug)
    print(f"Translated Spec-Kit '{slug}' → {contract_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover
        print(f"Translator failed: {exc}")
        raise
