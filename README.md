# Nexus Adjudicator — Project Law, Memory, and Momentum

**This is a ready-to-wire starter folder.** It includes LAW, gates, Spec‑Kit adapter, Translator stubs, Evidence pipeline, and CI. 
Anything not finished is clearly marked for **Codex** (see `CODEX_PROMPT.md`).

## Quick start
```bash
make up             # install tools (OPA/Trivy/OSV), set up pre-commit, sanity checks
make translate      # Spec‑Kit → artifacts (Product_Contract.json, Work_Order.md, diagrams)
make gate           # local PR Gate
make render         # convert .mmd → standalone HTML (and optional SVG)
make adopt repo=<URL>  # adopt an external repo (applies LAW + gates + spec seed)
```

## What’s here
- `AGENTS.md` + `NEXUS_LAW.md`: project law + workflow, machine-addressable markers
- `.nexus/config.yml`: single source of config (thresholds, globs, endpoints)
- `policy/*.rego`: OPA rules (layout / tests / secrets / license stub / coverage non-regression stub)
- `tools/`: gates, evidence collector, translator, diagram remediator, deploy/adopt helpers, CLI skeleton
- `.github/workflows/nexus-gate.yml`: CI with tests+coverage, OPA, Trivy, OSV, SBOM, PR/Release gate packets
- `web/`: a React wizard (Nexus Console) as a single component file to embed in your app

## What still needs Codex
- Wire real Spec‑Kit reading (we provide adapter + TODOs)
- Hook Wizard buttons to your backend (we provide frontend component + REST shapes)
- Expand OPA stubs (license/coverage rego) and add more rules if desired
- Optional: add OAuth (GitHub/GitLab) instead of PATs

**Date:** 2025-09-19
