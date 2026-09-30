#!/bin/sh
# print-handout.sh: print a lecture's handout to PDF with headless Chrome, in
# the same state the deck's own Handout button produces (handout layout plus
# study mode), so print can be checked without clicking through a print
# dialog. Optionally renders chosen pages to PNG so they can be looked at.
#
#   1. Serve the repo root on a port first:  python3 -m http.server 8765
#   2. scripts/print-handout.sh lectures/dsca-module-03.html OUT_DIR [PORT] [PAGES]
#        PAGES is a comma list, e.g. 3,4,7. Each becomes OUT_DIR/pN.png.
#
# macOS only (Google Chrome in /Applications; page rendering uses Swift and
# PDFKit, both built in). The temporary copy of the lecture is deleted again.
set -eu
DECK="$1"; OUT="$2"; PORT="${3:-8765}"; PAGES="${4:-}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mkdir -p "$OUT"
NAME="$(basename "$DECK" .html)"
TMP="$ROOT/lectures/_tmp-handout-$NAME.html"

# A copy of the deck that switches on handout layout and study mode at load.
python3 - "$ROOT/$DECK" "$TMP" <<'EOF'
import sys
s = open(sys.argv[1]).read()
s = s.replace('</body>', '<script>addEventListener("load",()=>{document.body.classList.add("lu-handout");window.LUDeck.deck.setSelfStudy(true,true)});</script></body>')
open(sys.argv[2], 'w').write(s)
EOF
trap 'rm -f "$TMP"' EXIT

"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=8000 \
  --print-to-pdf="$OUT/$NAME-handout.pdf" "http://localhost:$PORT/lectures/$(basename "$TMP")?cb=$$" 2>/dev/null
echo "wrote $OUT/$NAME-handout.pdf"

if [ -n "$PAGES" ]; then
  swift "$ROOT/scripts/pdf-pages.swift" "$OUT/$NAME-handout.pdf" "$OUT" "$PAGES"
fi
