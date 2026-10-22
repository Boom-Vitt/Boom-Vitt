"""Animated header/footer SVGs for the profile README (CSS animations run when GitHub shows an SVG as an image).

  python tools/profile_header.py assets tools/brand/face.jpg
"""
import base64
import math
import pathlib
import sys

OUT = pathlib.Path(sys.argv[1])
FACE = base64.b64encode(pathlib.Path(sys.argv[2]).read_bytes()).decode()
FONT = "Inter, 'Segoe UI', 'Helvetica Neue', Arial, 'Noto Sans Thai', 'Leelawadee UI', Thonburi, sans-serif"

PHRASES = [
    "สร้าง AI ภาษาไทยแบบโอเพนซอร์ส",
    "เจ้าของ Kruoop.com · Seeneo.ai",
    "Company OS (ERP) · Claude Code plugins",
    "BoomBigNose Lab — ASR ภาษาไทยถิ่น",
    "YouTube 220K · สอน AI ให้คนไทย",
]
N, STEP = len(PHRASES), 3.0  # seconds each phrase stays
CYCLE = N * STEP


def bars(x0, y_mid, n, gap, w, hmax, cls):
    out = []
    for i in range(n):
        h = 10 + hmax * abs(math.sin(i * 0.47) * math.cos(i * 0.13))
        out.append(f'<rect class="{cls}" style="animation-delay:-{(i * 0.11) % 1.6:.2f}s" x="{x0 + i * gap}" '
                   f'y="{y_mid - h / 2:.0f}" width="{w}" height="{h:.0f}" rx="{w / 2}"/>')
    return "".join(out)


phrase_css = []
phrase_svg = []
for i, p in enumerate(PHRASES):
    a, b = i * STEP / CYCLE * 100, (i + 1) * STEP / CYCLE * 100
    phrase_css.append(f"@keyframes p{i}{{0%,{max(a - 0.01, 0):.2f}%{{opacity:0;transform:translateY(10px)}}"
                      f"{a + 3:.2f}%,{b - 4:.2f}%{{opacity:1;transform:translateY(0)}}{b:.2f}%,100%{{opacity:0;transform:translateY(-10px)}}}}"
                      f".p{i}{{animation:p{i} {CYCLE}s infinite}}")
    phrase_svg.append(f'<text class="ph p{i}" x="400" y="236">{p}</text>')

header = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="380" viewBox="0 0 1200 380" role="img" aria-label="BoomBigNose — AI ภาษาไทย โอเพนซอร์ส">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1220"/><stop offset=".55" stop-color="#111a2e"/><stop offset="1" stop-color="#0d2230"/></linearGradient>
<radialGradient id="g1" cx=".82" cy=".2" r=".55"><stop offset="0" stop-color="#5eead4" stop-opacity=".30"/><stop offset="1" stop-color="#5eead4" stop-opacity="0"/></radialGradient>
<radialGradient id="g2" cx=".1" cy="1" r=".5"><stop offset="0" stop-color="#38bdf8" stop-opacity=".25"/><stop offset="1" stop-color="#38bdf8" stop-opacity="0"/></radialGradient>
<linearGradient id="title" x1="0" x2="1"><stop offset="0" stop-color="#e6edf7"/><stop offset=".5" stop-color="#a7f3d0"/><stop offset="1" stop-color="#e6edf7"/></linearGradient>
<clipPath id="card"><rect width="1200" height="380" rx="24"/></clipPath>
<clipPath id="av"><circle cx="190" cy="190" r="112"/></clipPath>
</defs>
<style>
text{{font-family:{FONT}}}
.k{{font-size:18px;font-weight:700;letter-spacing:.22em;fill:#5eead4}}
.t{{font-size:76px;font-weight:800;letter-spacing:-1.5px;fill:url(#title)}}
.l{{fill:#a7f3d0}}
.ph{{font-size:30px;font-weight:600;fill:#cbd5e1;opacity:0}}
.cur{{fill:#5eead4;animation:blink 1s steps(1) infinite}}
.bar{{fill:#5eead4;opacity:.22;transform-box:fill-box;transform-origin:center;animation:eq 1.6s ease-in-out infinite}}
.ring{{fill:none;stroke:#a7f3d0;stroke-width:3;opacity:.0;transform-origin:190px 190px;animation:ring 3s ease-out infinite}}
.glow{{animation:drift 9s ease-in-out infinite alternate}}
.in{{animation:rise 1.1s cubic-bezier(.2,.8,.2,1) both}}
@keyframes eq{{0%,100%{{transform:scaleY(.35)}}50%{{transform:scaleY(1)}}}}
@keyframes ring{{0%{{opacity:.55;transform:scale(1)}}100%{{opacity:0;transform:scale(1.35)}}}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes drift{{from{{transform:translate(0,0)}}to{{transform:translate(-60px,20px)}}}}
@keyframes rise{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:translateY(0)}}}}
{''.join(phrase_css)}
@media (prefers-reduced-motion:reduce){{.bar,.ring,.glow,.cur,.in{{animation:none}}.ph{{opacity:0}}.p0{{animation:none;opacity:1}}}}
</style>
<g clip-path="url(#card)">
<rect width="1200" height="380" fill="url(#bg)"/>
<rect class="glow" x="-100" y="-40" width="1400" height="460" fill="url(#g1)"/>
<rect width="1200" height="380" rx="24" fill="url(#g2)"/>
<g>{bars(640, 318, 30, 18, 9, 70, "bar")}</g>
</g>
<circle class="ring" cx="190" cy="190" r="128"/>
<circle class="ring" style="animation-delay:1.5s" cx="190" cy="190" r="128"/>
<circle cx="190" cy="190" r="118" fill="none" stroke="#5eead4" stroke-width="5"/>
<image href="data:image/jpeg;base64,{FACE}" x="78" y="78" width="224" height="224" clip-path="url(#av)"/>
<g class="in"><text class="k" x="400" y="110">BOOMBIGNOSE · BOOM-VITT</text>
<text class="t" x="396" y="182">BoomBigNose<tspan class="l"> ✦</tspan></text></g>
{''.join(phrase_svg)}
<g class="in" style="animation-delay:.3s"><text x="400" y="292" font-size="20" fill="#94a3b8">🇹🇭 Founder · Kruoop.com · Seeneo.ai  ·  YouTube 220K  ·  Open source</text></g>
</svg>
"""

footer = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="120" viewBox="0 0 1200 120" role="img" aria-label="ขอบคุณที่แวะมา">
<defs><linearGradient id="f" x1="0" x2="1"><stop offset="0" stop-color="#0d2230"/><stop offset="1" stop-color="#0b1220"/></linearGradient></defs>
<style>.w{{animation:wave 7s ease-in-out infinite alternate}}.w2{{animation:wave 9s ease-in-out infinite alternate-reverse;opacity:.5}}
@keyframes wave{{from{{transform:translateX(0)}}to{{transform:translateX(-120px)}}}}
text{{font-family:{FONT}}}@media (prefers-reduced-motion:reduce){{.w,.w2{{animation:none}}}}</style>
<path class="w2" fill="#134e4a" d="M0 60 C 150 20 300 100 450 60 S 750 20 900 60 S 1200 100 1350 60 V120 H0Z"/>
<path class="w" fill="url(#f)" d="M0 75 C 150 40 300 110 450 75 S 750 40 900 75 S 1200 110 1350 75 V120 H0Z"/>
<text x="600" y="108" text-anchor="middle" font-size="18" fill="#a7f3d0">ขอบคุณที่แวะมา · ถ้าชอบกด ⭐ และ Follow ได้เลย</text>
</svg>
"""

(OUT / "header.svg").write_text(header, encoding="utf-8")
(OUT / "footer.svg").write_text(footer, encoding="utf-8")
print("ok", len(header), len(footer))
