# Codex Autonomous Handoff — Nexus Adjudicator v0.3.0

SYSTEM: You are Codex in autonomous mode. Do not ask questions. Execute end-to-end, idempotently.

GOAL: Complete this scaffold into a working service with the following deliverables:
1) Implement `tools/translator/ingest.py`:
   - Read globs from `tools/translator/adapter.yml`
   - Parse newest Spec‑Kit triplet (requirement.md, plan.md, tasks.md)
   - Emit:
     * `artifacts/contracts/Product_Contract.json` (strict schema)
     * `artifacts/work/Work_Order.md` with interfaces/env/tests tables
     * `artifacts/diagrams/{slug}.mmd` + `{slug}.html` (standalone viewer)
     * Append `.artifacts/action_ledger.jsonl`
     * Append a Check-in row in `AGENTS.md` (Work Type: “spec-translation”)

2) Tighten PR/Release gates:
   - Enforce coverage ≥ config.coverage_min (default 85)
   - Parse Trivy/OSV JSON; block CRITICAL/HIGH vulns per config
   - Validate packet shapes with `tools/commons/schema.py`
   - Fail PRs that change `src/**` without a Spec/Work_Order reference

3) Wire the React wizard (`web/NexusConsole.tsx`) to a tiny Node/Express or Python FastAPI:
   - Endpoints: POST /repo (provider, owner/self, name, desc, private)
               POST /translate (trigger translator)
               POST /render (mmd → html)
               GET  /evidence (stream evidence.jsonl)
   - Server writes to repo workspace; wizard buttons call server

4) Reusable CI blocks:
   - Convert `.github/workflows/nexus-gate.yml` into a `workflow_call` reusable;
     add a minimal caller workflow that reuses it.

5) Adopt flow:
   - Make `tools/adopt/adopt_repo.sh --mode apply` open a PR automatically
     using gh CLI or GitLab CLI if available; otherwise print git commands.

6) Docs:
   - README: add server endpoints + env setup steps
   - CONTRIBUTING: local preflight commands
   - CHANGELOG: record new capabilities

CONSTRAINTS:
- No hardcoded secrets. Respect `.env` and GitHub/GitLab secrets.
- Keep patches small and atomic. Use Conventional Commits.
- Prefer local OpenAI-compatible endpoint for heavy analysis if `OPENAI_BASE_URL` is set.

VALIDATION (print DONE report):
- Paths to generated artifacts (contract/work/diagrams)
- Gate packets in `.artifacts/gate_reports/*.json`
- Evidence files and Expectation Card
- API server running locally with the listed endpoints
