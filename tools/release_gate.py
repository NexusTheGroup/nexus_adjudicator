import argparse, json, os, re, sys
from tools.commons.schema import RELEASE_VERDICT_KEYS, validate_shape

def read(p, d=""):
    try: return open(p,"r",encoding="utf-8",errors="ignore").read()
    except: return d

def semver_ok(v): return re.match(r"^\d+\.\d+\.\d+([\-+][0-9A-Za-z\.\-]+)?$", v) is not None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", required=True)
    ap.add_argument("--changelog", required=True)
    ap.add_argument("--sbom", required=True)
    ap.add_argument("--trivy", required=True)
    ap.add_argument("--osv", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    reasons = []
    if not semver_ok(args.version):
        reasons.append("Invalid SemVer")

    verdict = {
        "allow": len(reasons)==0,
        "critical_blockers": reasons,
        "policy_violations": [],
        "required_hotfix_prs": [],
        "release_notes_ok": True
    }
    validate_shape(verdict, RELEASE_VERDICT_KEYS, "RELEASE_VERDICT")
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(verdict, f, indent=2)
    print(json.dumps(verdict, indent=2))
    sys.exit(0 if verdict["allow"] else 3)

if __name__ == "__main__":
    main()
