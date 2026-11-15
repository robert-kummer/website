#!/bin/sh
# Rendert tools/og-image.html mit Chrome headless zu src/assets/img/og-image.jpg (1200 × 630).
# Nur nötig, wenn sich Text oder Foto ändern. Das Ergebnis wird eingecheckt, der Build braucht kein Chrome.
set -eu
cd "$(dirname "$0")/.."
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
tmp="$(mktemp -d)"
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --window-size=1200,630 --virtual-time-budget=3000 \
  --screenshot="$tmp/og.png" "file://$PWD/tools/og-image.html" 2>/dev/null
sips -s format jpeg -s formatOptions 85 "$tmp/og.png" --out src/assets/img/og-image.jpg >/dev/null
rm -rf "$tmp"
sips -g pixelWidth -g pixelHeight src/assets/img/og-image.jpg
