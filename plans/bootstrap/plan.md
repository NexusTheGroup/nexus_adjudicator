# Bootstrap Plan — Nexus Translator & Console

## Interfaces
- make translate: Runs translator pipeline for the latest Spec-Kit.
- POST /translate: Triggers translator ingestion via the backend service.
- POST /render: Converts mermaid diagrams to standalone HTML.
- GET /evidence: Streams accumulated evidence packets for audits.

## Environments
- local-dev: Developer laptop with Python 3.10+ and Node 18.
- ci: GitHub Actions or comparable runner executing nexus-gate workflow.

## Tests
- python3 -m py_compile tools/translator/ingest.py: Syntax check translator.
- npm test -- --watch=false: Placeholder for future frontend tests.
