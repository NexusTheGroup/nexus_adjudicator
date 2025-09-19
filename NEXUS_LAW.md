# NEXUS_LAW — Non-negotiable
<!-- >>LAW:STANDARDS:BEGIN -->
- Conventional Commits; SemVer; Keep a Changelog; CODEOWNERS
- OPA/Rego policy pass required
- Coverage threshold obeyed; no critical/high vulns
- Evidence logged; SBOM produced
<!-- >>LAW:STANDARDS:END -->

<!-- >>LAW:PR_GATE:BEGIN -->
PR Gate JSON:
{ "pass": true|false, "reasons":[], "required_fixes":[], "inline_comments":[], "coverage_delta":"", "policy":{"opa_pass":true,"violations":[]}, "vuln":{"critical":0,"high":0,"osv_total":0} }
<!-- >>LAW:PR_GATE:END -->

<!-- >>LAW:RELEASE_GATE:BEGIN -->
Release Gate JSON:
{ "allow": true|false, "critical_blockers":[], "policy_violations":[], "required_hotfix_prs":[], "release_notes_ok": true|false }
<!-- >>LAW:RELEASE_GATE:END -->
