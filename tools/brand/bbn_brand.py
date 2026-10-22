"""BoomBigNose repo branding: a unique animated banner per repo plus a README header/footer between markers.

  python tools/brand/bbn_brand.py <spec.json> <repo-name> <checkout-dir>

Idempotent: re-running replaces the marked blocks and the banner file only.
"""
import base64
import html
import json
import math
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
FACE = base64.b64encode((HERE / "face.jpg").read_bytes()).decode()
FONT = "Inter, 'Segoe UI', 'Helvetica Neue', Arial, 'Noto Sans Thai', 'Leelawadee UI', Thonburi, sans-serif"
CATS = {  # accent colour, kicker label
    "claude-code": ("#E8906F", "CLAUDE CODE"),
    "ai-ml": ("#5EEAD4", "AI · ML"),
    "web": ("#38BDF8", "WEB"),
    "video-3d": ("#A78BFA", "VIDEO · 3D"),
    "business": ("#FBBF24", "BUSINESS"),
    "guide": ("#34D399", "GUIDE"),
    "automation": ("#F472B6", "AUTOMATION"),
    "learning-project": ("#94A3B8", "LEARNING"),
}
H_START, H_END = "<!-- BBN:HEADER:START -->", "<!-- BBN:HEADER:END -->"
F_START, F_END = "<!-- BBN:FOOTER:START -->", "<!-- BBN:FOOTER:END -->"
# a top-of-README hero image the banner replaces (local banner/hero files, AI Studio "GHBanner" template)
HERO = re.compile(r'^\s*(<img [^>]*(src="(assets|docs/assets)/(banner|hero)\.[a-z]+"|alt="GHBanner")[^>]*/?>|!\[[^\]]*\]\(assets/banner\.png\))\s*$', re.I)


def esc(s):
    return html.escape(s or "", quote=True)


def banner_svg(s):
    accent, kicker = CATS.get(s["category"], CATS["learning-project"])
    title = s["title"]
    tsize = 60 if len(title) <= 16 else 52 if len(title) <= 22 else 44
    bars = "".join(
        f'<rect class="b" style="animation-delay:-{(i * .13) % 1.7:.2f}s" x="{760 + i * 16}" y="{246 - h / 2:.0f}" width="8" '
        f'height="{h:.0f}" rx="4"/>'
        for i, h in ((i, 8 + 46 * abs(math.sin(i * .51 + len(title)) * math.cos(i * .17))) for i in range(26)))
    chips, x = [], 300
    for c in s.get("chips", [])[:3]:
        w = 22 + 10.5 * len(c)
        chips.append(f'<rect x="{x}" y="226" width="{w:.0f}" height="34" rx="17" fill="#ffffff" fill-opacity=".06" stroke="{accent}" '
                     f'stroke-opacity=".45"/><text x="{x + w / 2:.0f}" y="249" text-anchor="middle" class="c">{esc(c)}</text>')
        x += w + 10
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="300" viewBox="0 0 1200 300" role="img" aria-label="{esc(title)} — {esc(s.get('tagline_en'))}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1220"/><stop offset=".6" stop-color="#111a2e"/><stop offset="1" stop-color="#0d1b2a"/></linearGradient>
<radialGradient id="gl" cx=".85" cy=".15" r=".6"><stop offset="0" stop-color="{accent}" stop-opacity=".28"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
<clipPath id="card"><rect width="1200" height="300" rx="22"/></clipPath><clipPath id="face"><circle cx="150" cy="150" r="96"/></clipPath>
</defs>
<style>text{{font-family:{FONT}}}.k{{font-size:16px;font-weight:700;letter-spacing:.2em;fill:{accent}}}.t{{font-size:{tsize}px;font-weight:800;letter-spacing:-1px;fill:#eef2f8}}
.th{{font-size:24px;font-weight:600;fill:#cbd5e1}}.en{{font-size:18px;fill:#8b9bb4}}.c{{font-size:15px;font-weight:600;fill:#e2e8f0}}.u{{font-size:13px;fill:#64748b}}
.b{{fill:{accent};opacity:.25;transform-box:fill-box;transform-origin:center;animation:eq 1.7s ease-in-out infinite}}
.r{{fill:none;stroke:{accent};stroke-width:3;transform-origin:150px 150px;animation:rg 3.2s ease-out infinite}}.g{{animation:dr 10s ease-in-out infinite alternate}}
@keyframes eq{{0%,100%{{transform:scaleY(.35)}}50%{{transform:scaleY(1)}}}}@keyframes rg{{0%{{opacity:.6;transform:scale(1)}}100%{{opacity:0;transform:scale(1.3)}}}}
@keyframes dr{{from{{transform:translate(0,0)}}to{{transform:translate(-50px,18px)}}}}
@media (prefers-reduced-motion:reduce){{.b,.r,.g{{animation:none}}}}</style>
<g clip-path="url(#card)"><rect width="1200" height="300" fill="url(#bg)"/><rect class="g" x="-80" y="-30" width="1360" height="360" fill="url(#gl)"/>{bars}</g>
<circle class="r" cx="150" cy="150" r="100"/><circle cx="150" cy="150" r="102" fill="none" stroke="{accent}" stroke-width="4"/>
<image href="data:image/jpeg;base64,{FACE}" x="54" y="54" width="192" height="192" clip-path="url(#face)"/>
<text class="k" x="300" y="72">BOOMBIGNOSE · {kicker}</text>
<text class="t" x="296" y="{72 + tsize + 4}">{esc(title)}</text>
<text class="th" x="300" y="{72 + tsize + 44}">{esc(s.get('tagline_th'))}</text>
<text class="en" x="300" y="{72 + tsize + 72}">{esc(s.get('tagline_en'))}</text>
{''.join(chips)}
<text class="u" x="1180" y="284" text-anchor="end">github.com/Boom-Vitt/{esc(s['name'])}</text>
</svg>
"""


def header(s, branch):
    n = s["name"]
    return f"""{H_START}
<div align="center">

<img src=".github/brand/banner.svg" width="100%" alt="{esc(s['title'])} — {esc(s.get('tagline_en'))}" />

<a href="https://github.com/Boom-Vitt/{n}/stargazers"><img src="https://img.shields.io/github/stars/Boom-Vitt/{n}?style=flat-square&color=14b8a6&labelColor=0b1220" alt="stars" /></a>
<a href="https://github.com/Boom-Vitt/{n}/commits/{branch}"><img src="https://img.shields.io/github/last-commit/Boom-Vitt/{n}?style=flat-square&color=14b8a6&labelColor=0b1220" alt="last commit" /></a>
<a href="https://github.com/Boom-Vitt"><img src="https://img.shields.io/badge/by-BoomBigNose-14b8a6?style=flat-square&labelColor=0b1220" alt="by BoomBigNose" /></a>

</div>
{H_END}
"""


FOOTER = f"""{F_START}
---

<div align="center">

**สร้างโดย [BoomBigNose](https://github.com/Boom-Vitt)** · [Kruoop.com](https://kruoop.com) แหล่งเรียน AI + คอมมูนิตี้ · [Seeneo.ai](https://seeneo.ai) · [YouTube 220K](https://www.youtube.com/@BoomBigNose)

<sub>ถ้าโปรเจกต์นี้มีประโยชน์ กด ⭐ ให้กำลังใจกันได้เลย</sub>

</div>
{F_END}
"""


def apply_readme(text, s, branch):
    text = re.sub(re.escape(H_START) + r".*?" + re.escape(H_END) + r"\n?", "", text, flags=re.S)
    text = re.sub(r"\n*" + re.escape(F_START) + r".*?" + re.escape(F_END) + r"\n?", "\n", text, flags=re.S)
    lines = text.splitlines()
    for i, line in enumerate(lines[:6]):  # drop an old top hero; the banner takes its place
        if HERO.match(line):
            del lines[i]
            break
    body = "\n".join(lines).strip("\n")
    if not body.strip():
        body = f"# {s['title']}\n\n{s.get('readme_stub_th') or s.get('description') or s.get('tagline_th')}"
    return header(s, branch) + "\n" + body + "\n\n" + FOOTER


def main():
    spec_path, name, repo_dir = sys.argv[1:4]
    s = next(x for x in json.load(open(spec_path, encoding="utf-8")) if x["name"] == name)
    d = pathlib.Path(repo_dir)
    branch = sys.argv[4] if len(sys.argv) > 4 else "main"
    (d / ".github/brand").mkdir(parents=True, exist_ok=True)
    (d / ".github/brand/banner.svg").write_text(banner_svg(s), encoding="utf-8")
    readme = next((p for p in d.iterdir() if p.name.lower() == "readme.md"), d / "README.md")
    old = readme.read_text(encoding="utf-8") if readme.exists() else ""
    readme.write_text(apply_readme(old, s, branch), encoding="utf-8")
    print(f"branded {name} -> {readme.name}")


if __name__ == "__main__":
    main()
