#!/usr/bin/env bash
set -euo pipefail
: "${APP_VERSION:=0.3.0}"
: "${ENVIRONMENT:=dev}"
: "${HEALTHCHECK_URL:=http://localhost:8000/health}"
render(){ envsubst < "$(dirname "$0")/manifest.yaml" > .artifacts/deploy_${ENVIRONMENT}.yaml; }
health(){ for i in {1..20}; do curl -fsS "$HEALTHCHECK_URL" && exit 0 || sleep 2; done; echo "unhealthy"; exit 1; }
mkdir -p .artifacts; render
echo "Dry-run deploy (set CONFIRM_DEPLOY=1 to apply)."
[[ "${CONFIRM_DEPLOY:-0}" == "1" ]] && kubectl apply -f ".artifacts/deploy_${ENVIRONMENT}.yaml" && health || true
