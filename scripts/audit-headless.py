#!/usr/bin/env python3
"""audit-headless.py: run scripts/audit-deck.js on a lecture with headless Chrome, no browser pane.

    python3 scripts/audit-headless.py lectures/dsca-module-03.html [PORT]

Needs the repository served over http first (python3 -m http.server 8765 from the repo root),
Google Chrome in /Applications (macOS), and nothing else. It makes a temporary copy of the lecture
that loads audit-deck.js after the deck boots and writes the report into the page, then removes the
copy. Prints the failing checks as JSON and exits 1 if any check fails. Study mode is cleared
first. Checks the same things as pasting audit-deck.js into the console (overflow, flow checks,
notes minutes, and so on); it does NOT click through quizzes, so still test answered MCQs.
"""
import json, os, re, subprocess, sys, tempfile

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
deck = sys.argv[1]
port = sys.argv[2] if len(sys.argv) > 2 else "8765"
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(root, deck), encoding="utf-8").read()
inject = """<script>
Object.keys(localStorage).filter(function(k){return k.indexOf('lu:')===0}).forEach(function(k){localStorage.removeItem(k)});
addEventListener('load', function(){ setTimeout(async function(){
  try {
    var code = await (await fetch('/scripts/audit-deck.js')).text();
    var r = await (0, eval)(code);
    var out = {}; Object.keys(r).forEach(function(k){ if (k !== 'tinyText' && r[k].length) out[k] = r[k]; });
    out._slides = document.querySelectorAll('.slide').length;
    document.body.setAttribute('data-audit', JSON.stringify(out));
  } catch (e) { document.body.setAttribute('data-audit', JSON.stringify({_error: String(e)})); }
}, 800); });
</script></body>"""
tmp_name = "_tmp-audit-%d.html" % os.getpid()
tmp_path = os.path.join(root, os.path.dirname(deck), tmp_name)
open(tmp_path, "w", encoding="utf-8").write(src.replace("</body>", inject, 1))
try:
    url = "http://localhost:%s/%s/%s?cb=%d" % (port, os.path.dirname(deck), tmp_name, os.getpid())
    dom = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=120000", "--dump-dom", url],
                         capture_output=True, text=True, timeout=300).stdout
finally:
    os.remove(tmp_path)
m = re.search(r"data-audit='([^']*)'|data-audit=\"([^\"]*)\"", dom)
if not m:
    print(json.dumps({"_error": "no audit result in the page (is the server running on port %s?)" % port})); sys.exit(2)
report = json.loads((m.group(1) or m.group(2)).replace("&quot;", '"').replace("&amp;", "&"))
print(json.dumps(report, indent=1))
sys.exit(1 if [k for k in report if not k.startswith("_")] else 0)
