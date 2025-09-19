import argparse, datetime as dt, hashlib, json, os
ART = ".artifacts"
def ensure(): os.makedirs(ART, exist_ok=True)
def fp(msg, top=""): return hashlib.sha256((msg or "" + "|" + top).encode()).hexdigest()[:12]
def append(record: dict, path=f"{ART}/evidence.jsonl"):
    ensure(); record["ts"] = dt.datetime.now().isoformat()
    with open(path,"a",encoding="utf-8") as f: f.write(json.dumps(record)+"\n")
def rotate():
    path = f"{ART}/evidence.jsonl"
    if os.path.exists(path):
        newp = f"{ART}/evidence-{dt.datetime.now().strftime('%Y%m%d')}.jsonl"
        if not os.path.exists(newp): os.replace(path, newp)
def card(src=f"{ART}/evidence.jsonl", out=f"{ART}/expectation_card.md"):
    rows = []
    if os.path.exists(src):
        for line in open(src, "r", encoding="utf-8", errors="ignore"):
            try: rows.append(json.loads(line))
            except: pass
    freq = {}
    for r in rows:
        ex = r.get("exception") or {}
        h = fp(ex.get("message",""), ex.get("stack_top",""))
        freq[h] = freq.get(h, 0) + 1
    with open(out, "w", encoding="utf-8") as f:
        f.write("# Expectation Card (Auto)\n\n")
        if not freq: f.write("_No recurring fingerprints yet._\n"); return
        for k,n in sorted(freq.items(), key=lambda x: x[1], reverse=True)[:10]:
            f.write(f"- **{k}** ×{n} — prechecks/tests recommended.\n")
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--make-expectation-card", action="store_true")
    a = ap.parse_args()
    if a.make_expectation_card: card()
    else: rotate()
