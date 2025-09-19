import sys, os
TEMPLATE = '''<!doctype html><meta charset="utf-8"><title>Diagram</title>
<div class="mermaid">%s</div>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>mermaid.initialize({startOnLoad:true, securityLevel:"loose"});</script>'''
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: remediate.py input.mmd output.html"); sys.exit(1)
    src, out = sys.argv[1], sys.argv[2]
    text = open(src, "r", encoding="utf-8").read()
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    open(out, "w", encoding="utf-8").write(TEMPLATE % text.replace("`","\u0060"))
    print("wrote", out)
