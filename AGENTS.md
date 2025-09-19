# Nexus Adjudicator — Project Law, Memory, and Momentum
<!-- UNRELATED to Sonatype Nexus Repository. -->

<!-- >>ROW:ROW_INDEX:BEGIN -->
## Row Index (machine-addressable)
| ID | Purpose | Begin | End |
|---|---|---|---|
| MUST_READ | must-read ranges | `>>ROW:MUST_READ:BEGIN` | `>>ROW:MUST_READ:END` |
| CHECKIN | check-in/out log | `>>ROW:CHECKIN:BEGIN` | `>>ROW:CHECKIN:END` |
| GUARDRAILS | standards | `>>ROW:GUARDRAILS:BEGIN` | `>>ROW:GUARDRAILS:END` |
| WORKFLOW | stages | `>>ROW:WORKFLOW:BEGIN` | `>>ROW:WORKFLOW:END` |
| SCORING | rubric | `>>ROW:SCORING:BEGIN` | `>>ROW:SCORING:END` |
<!-- >>ROW:ROW_INDEX:END -->

<!-- >>ROW:MUST_READ:BEGIN -->
Read GUARDRAILS, WORKFLOW, SCORING before any work.
<!-- >>ROW:MUST_READ:END -->

<!-- >>ROW:CHECKIN:BEGIN -->
## Check-in / Check-out (append-only)
Timezone: America/Chicago
| AI Name | Model | Session ID | Login (ISO) | Work Type | Files/Areas | Logout (ISO) | Summary | Self-Score |
|---|---|---|---|---|---|---|---|---|
| Codex | GPT-5 | sess-20250919011910 | 2025-09-19T01:19:10-05:00 | spec-translation | bootstrap |  | Translated bootstrap Spec-Kit | - |
<!-- >>ROW:CHECKIN:END -->

<!-- >>ROW:GUARDRAILS:BEGIN -->
## Guardrails
1. Commits: Conventional; Versions: SemVer; Releases: Keep a Changelog; Ownership via CODEOWNERS.
2. PR Gate required; failing code sent to Trashbin with grade.
3. OPA/Rego policies run locally & CI.
4. Evidence must be recorded (JUnit, coverage, SBOM, scans).
<!-- >>ROW:GUARDRAILS:END -->

<!-- >>ROW:WORKFLOW:BEGIN -->
## Workflow
Intake → Plan → Build (small PRs) → Validate & Ship (gates) → Evidence & Expectation Cards.
<!-- >>ROW:WORKFLOW:END -->

<!-- >>ROW:SCORING:BEGIN -->
## Scoring
PASS ≥85, 70–84 revise, <70 Trashbin.
<!-- >>ROW:SCORING:END -->
