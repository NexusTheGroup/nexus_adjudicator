#!/usr/bin/env bash
set -euo pipefail
echo "Installing tools (best-effort)…"
which opa >/dev/null 2>&1 || (curl -L -o opa https://openpolicyagent.org/downloads/latest/opa_linux_amd64 && chmod +x opa && sudo mv opa /usr/local/bin/opa || true)
which trivy >/dev/null 2>&1 || echo "Install Trivy manually (see README)."
which osv-scanner >/dev/null 2>&1 || echo "Install OSV-Scanner manually (see README)."
echo "Setting up pre-commit (optional)…"
if which pre-commit >/dev/null 2>&1; then pre-commit install || true; fi
echo "✔ nexus ready"
