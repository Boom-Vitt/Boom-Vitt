"""Product banners and marker-based README headers/footers for BoomBigNose repos.

  python tools/brand/bbn_brand.py <spec.json> <repo-name> <checkout-dir>

Idempotent: re-running replaces the marked blocks and the banner file only.
"""
import html
import json
import pathlib
import re
import sys

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
    chips, x = [], 52
    for c in s.get("chips", [])[:3]:
        w = 22 + 10.5 * len(c)
        chips.append(f'<rect x="{x}" y="226" width="{w:.0f}" height="34" rx="17" fill="#ffffff" fill-opacity=".06" stroke="{accent}" '
                     f'stroke-opacity=".45"/><text x="{x + w / 2:.0f}" y="249" text-anchor="middle" class="c">{esc(c)}</text>')
        x += w + 10
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="300" viewBox="0 0 1200 300" role="img" aria-label="{esc(title)} · {esc(s.get('tagline_en'))}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1220"/><stop offset=".6" stop-color="#111a2e"/><stop offset="1" stop-color="#0d1b2a"/></linearGradient>
<radialGradient id="gl" cx=".85" cy=".15" r=".6"><stop offset="0" stop-color="{accent}" stop-opacity=".28"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#5eead4" stroke-opacity=".06"/></pattern>
<clipPath id="card"><rect width="1200" height="300" rx="22"/></clipPath>
</defs>
<style>text{{font-family:{FONT}}}.k{{font-size:16px;font-weight:700;letter-spacing:.2em;fill:{accent}}}.t{{font-size:{tsize}px;font-weight:800;letter-spacing:-1px;fill:#eef2f8}}
.th{{font-size:24px;font-weight:600;fill:#cbd5e1}}.en{{font-size:18px;fill:#8b9bb4}}.c{{font-size:15px;font-weight:600;fill:#e2e8f0}}.u{{font-size:13px;fill:#94a3b8}}</style>
<g clip-path="url(#card)"><rect width="1200" height="300" fill="url(#bg)"/><rect width="1200" height="300" fill="url(#gl)"/><rect width="1200" height="300" fill="url(#grid)"/></g>
<rect x="28" y="42" width="4" height="218" rx="2" fill="{accent}"/>
<text class="k" x="52" y="58">{kicker}</text>
<text class="t" x="50" y="122">{esc(title)}</text>
<text class="th" x="52" y="166">{esc(s.get('tagline_th'))}</text>
<text class="en" x="52" y="198">{esc(s.get('tagline_en'))}</text>
{''.join(chips)}
<text class="u" x="1180" y="284" text-anchor="end">github.com/Boom-Vitt/{esc(s['name'])}</text>
</svg>
"""


def header(s, branch):
    return f"""{H_START}
<img src=".github/brand/banner.svg" width="100%" alt="{esc(s['title'])} · {esc(s.get('tagline_en'))}" />
{H_END}
"""


FOOTER = f"""{F_START}
[Made by BoomBigNose](https://github.com/Boom-Vitt)
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
