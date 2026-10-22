"""Generate the static profile banner: python3 tools/profile_header.py assets."""
import pathlib
import sys

FONT = "Inter, 'Segoe UI', 'Helvetica Neue', Arial, 'Noto Sans Thai', 'Leelawadee UI', Thonburi, sans-serif"

header = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="180" viewBox="0 0 1200 180" role="img" aria-label="BoomBigNose · AI ภาษาไทย · Open source">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1220"/><stop offset="1" stop-color="#0d2230"/></linearGradient>
</defs>
<rect width="1200" height="180" rx="18" fill="url(#bg)"/>
<rect x="40" y="38" width="5" height="104" rx="2" fill="#5eead4"/>
<g font-family="{FONT}">
<text x="68" y="91" font-size="56" font-weight="800" fill="#eef2f8">BoomBigNose</text>
<text x="70" y="132" font-size="24" fill="#a7f3d0">AI ภาษาไทย · Open source</text>
</g>
</svg>
"""

out = pathlib.Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
(out / "header.svg").write_text(header, encoding="utf-8")
print("generated", out / "header.svg")
