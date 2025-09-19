---
title: Nexus Translator & Console Workstream
owner: Platform Enablement
---

# Nexus Translator & Console

## Summary
Deliver the first translator pipeline, service APIs, and console wiring so teams can adopt Nexus Adjudicator without manual scaffolding.

## Actors
- Platform engineers
- Release managers
- Application teams

## Acceptance Criteria
- Translator emits Product_Contract, Work_Order, diagrams, & ledger entries.
- Ledger and AGENTS.md check-in capture translation runs.
- React console flows execute via backend service endpoints.

## Non Goals
- Cloud deployment automation.
- Multi-tenant auth or RBAC.

## Dependencies
- Python 3.10+
- Node 18+
- GitHub CLI for optional PR automation.

## Risks
- Missing spec kits halting translation.
- Misconfigured CI gating blocking releases.
