# Work Order — Nexus Translator & Console Workstream

_Generated 2025-09-19T06:19:10Z from `bootstrap` Spec-Kit._

## Interfaces
| Interface | Notes |
| --- | --- |
| make translate | Runs translator pipeline for the latest Spec-Kit. |
| POST /translate | Triggers translator ingestion via the backend service. |
| POST /render | Converts mermaid diagrams to standalone HTML. |
| GET /evidence | Streams accumulated evidence packets for audits. |

## Environments
| Environment | Details |
| --- | --- |
| local-dev | Developer laptop with Python 3.10+ and Node 18. |
| ci | GitHub Actions or comparable runner executing nexus-gate workflow. |

## Tests
| Test | Coverage / Target |
| --- | --- |
| Unit tests for translator ingest.py | Validate contract generation, work order tables, diagram creation. |
| Integration tests for backend service | Endpoint responses, file writes, error handling. |
| E2E tests for console wiring | Button clicks trigger server calls, UI updates reflect backend state. |

## Summary
Deliver the first translator pipeline, service APIs, and console wiring so teams can adopt Nexus Adjudicator without manual scaffolding.
