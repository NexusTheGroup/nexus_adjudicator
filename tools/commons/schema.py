PR_VERDICT_KEYS = {
    "pass": bool, "reasons": list, "required_fixes": list, "inline_comments": list,
    "coverage_delta": str, "policy": dict, "vuln": dict
}
RELEASE_VERDICT_KEYS = {
    "allow": bool, "critical_blockers": list, "policy_violations": list,
    "required_hotfix_prs": list, "release_notes_ok": bool
}
def validate_shape(obj: dict, shape: dict, name="packet"):
    missing = [k for k in shape if k not in obj]
    wrong = [k for k,t in shape.items() if k in obj and not isinstance(obj[k], t)]
    if missing or wrong:
        raise ValueError(f"{name} invalid: missing={missing} wrong_types={wrong}")
