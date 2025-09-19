#!/usr/bin/env bash
set -euo pipefail
usage(){ echo "adopt_repo.sh --repo <url> --mode plan|apply"; exit 1; }
REPO="" MODE="plan"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo) REPO="$2"; shift 2;;
    --mode) MODE="$2"; shift 2;;
    *) usage;;
  esac
done
[[ -z "$REPO" ]] && usage
TMP="$(mktemp -d)"
echo "Cloning $REPO into $TMP"; git clone --depth 1 "$REPO" "$TMP"
echo "== Plan =="
echo "- Merge AGENTS.md / NEXUS_LAW.md, wire CI + OPA + gates"
if [[ "$MODE" == "apply" ]]; then
  cp -f AGENTS.md NEXUS_LAW.md "$TMP"/
  mkdir -p "$TMP/.github/workflows" "$TMP/policy" "$TMP/tools"
  cp -r .github/workflows/nexus-gate.yml "$TMP/.github/workflows/"
  cp -r policy/* "$TMP/policy/"
  cp -r tools "$TMP/tools/"
  (cd "$TMP" && git checkout -b chore/nexus-law && git add . && git commit -m "chore(nexus): scaffold law + gates" && echo "Open PR in $TMP")
fi
