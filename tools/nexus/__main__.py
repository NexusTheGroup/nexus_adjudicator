import typer, os, subprocess, sys
app = typer.Typer(help="Nexus CLI (starter)")

@app.command()
def translate():
    """Spec‑Kit → artifacts (handoff stub)."""
    subprocess.run([sys.executable, "tools/translator/ingest.py"], check=False)

@app.command()
def gate():
    """Run local PR Gate."""
    subprocess.run([sys.executable, "tools/pr_gate.py", "--changed", ".artifacts/opa_input.json", "--junit", ".artifacts/junit.xml", "--coverage", ".artifacts/coverage.json", "--opa", ".artifacts/opa_report.json", "--trivy", ".artifacts/vuln/trivy.json", "--osv", ".artifacts/vuln/osv.json", "--out", ".artifacts/gate_reports/pr_gate.json"], check=False)

@app.command()
def render():
    """Render .mmd to standalone HTML (simple)."""
    os.makedirs("artifacts/diagrams", exist_ok=True)
    for root,_,files in os.walk("artifacts/diagrams"):
        for f in files:
            if f.endswith(".mmd"):
                src = os.path.join(root, f)
                out = src.replace(".mmd",".html")
                subprocess.run([sys.executable, "tools/diagrams/remediate.py", src, out], check=False)

@app.command()
def adopt(repo: str):
    """Adopt a repo (stub)."""
    subprocess.run(["bash", "tools/adopt/adopt_repo.sh", "--repo", repo, "--mode", "plan"], check=False)

@app.command()
def new(owner: str, name: str):
    """Create new repo via wizard UI (use frontend) or script (TODO)."""
    typer.echo("Use the GUI wizard or provide a PAT to script creation.")

if __name__ == "__main__":
    app()
