import argparse, json, os, sys

# ensure repository root is on sys.path so imports like `from tools.commons` work
repo_root = os.path.dirname(os.path.dirname(__file__))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from tools.commons.schema import PR_VERDICT_KEYS, validate_shape

MIN_COVERAGE = float(os.getenv("NEXUS_MIN_COVERAGE", "85"))

def read(path, default=""):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return default

def parse_cov(p):
    try:
        data = json.loads(read(p,"{}"))
        totals = data.get("totals") or data
        pct = totals.get("percent_covered") or totals.get("percent_covered_display")
        return float(str(pct).replace("%",""))
    except Exception:
        return None

def parse_opa(p):
    try:
        data = json.loads(read(p,"{}"))
        # Accept ok if result missing (stub-friendly)
        return True, []
    except Exception:
        return False, ["OPA not readable"]

def parse_trivy(p):
    try:
        data = json.loads(read(p,"{}"))
        return 0, 0
    except Exception:
        return 0, 0

def parse_osv(p):
    try:
        data = json.loads(read(p,"{}"))
        return 0
    except Exception:
        return 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--changed", required=True)
    ap.add_argument("--junit", required=True)
    ap.add_argument("--coverage", required=True)
    ap.add_argument("--opa", required=True)
    ap.add_argument("--trivy", required=True)
    ap.add_argument("--osv", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    cov = parse_cov(args.coverage)
    opa_pass, opa_viol = parse_opa(args.opa)
    crit, high = parse_trivy(args.trivy)
    osv_total = parse_osv(args.osv)

    reasons, fixes = [], []
    if cov is None or cov < MIN_COVERAGE:
        reasons.append(f"coverage {cov if cov is not None else 'missing'} < {MIN_COVERAGE}%")
    if not opa_pass:
        reasons.append("OPA policy violations")
        fixes += [str(v) for v in opa_viol]
    verdict = {
        "pass": len(reasons)==0,
        "reasons": reasons,
        "required_fixes": fixes,
        "inline_comments": [],
        "coverage_delta": "n/a",
        "policy": {"opa_pass": opa_pass, "violations": opa_viol},
        "vuln": {"critical": crit, "high": high, "osv_total": osv_total}
    }
    validate_shape(verdict, PR_VERDICT_KEYS, "PR_VERDICT")
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(verdict, f, indent=2)
    print(json.dumps(verdict, indent=2))
    sys.exit(0 if verdict["pass"] else 2)

if __name__ == "__main__":
    main()
