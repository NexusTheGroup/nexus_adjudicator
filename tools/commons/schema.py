PR_VERDICT_KEYS = {
    "pass": bool, "reasons": list, "required_fixes": list, "inline_comments": list,
    "coverage_delta": str, "policy": dict, "vuln": dict
}
RELEASE_VERDICT_KEYS = {
    "allow": bool, "critical_blockers": list, "policy_violations": list,
    "required_hotfix_prs": list, "release_notes_ok": bool
}
PRODUCT_CONTRACT_SCHEMA = {
    "product": {
        "title": str,
        "summary": str,
        "actors": list,
        "acceptance_criteria": list,
        "non_goals": list,
        "dependencies": list,
        "risks": list,
    },
    "source": {
        "requirement": str,
        "plan": str,
        "tasks": str,
    },
    "metadata": {
        "adapter": str,
        "generated_at": str,
        "slug": str,
    },
}
def validate_shape(obj: dict, shape: dict, name="packet"):
    missing = []
    wrong = []
    for k, expected in shape.items():
        if k not in obj:
            missing.append(k)
            continue
        actual = obj[k]
        if isinstance(expected, dict):
            if not isinstance(actual, dict):
                wrong.append(k)
            else:
                # Recurse
                sub_missing, sub_wrong = validate_shape(actual, expected, f"{name}.{k}")
                missing.extend(sub_missing)
                wrong.extend(sub_wrong)
        elif isinstance(expected, type):
            if not isinstance(actual, expected):
                wrong.append((k, type(actual).__name__, expected.__name__))
        else:
            # For other cases, perhaps check exact type or something, but for now assume type
            pass
    if missing or wrong:
        raise ValueError(f"{name} invalid: missing={missing} wrong_types={wrong}")
    return missing, wrong

def validate_product_contract(contract: dict) -> None:
    validate_shape(contract, PRODUCT_CONTRACT_SCHEMA, "Product_Contract")
    # Also validate nested shapes if needed, but for now basic
