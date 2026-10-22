"""python tools/brand/test_bbn_brand.py — self-check for the README rewrite (no network)."""
import xml.dom.minidom

import bbn_brand as b

S = {"name": "demo", "title": "Demo Repo", "tagline_th": "ทดสอบ", "tagline_en": "test", "category": "web", "chips": ["A", "B"]}

once = b.apply_readme('<img src="assets/banner.svg" alt="x" />\n\n# Demo\n\nbody\n', S, "main")
twice = b.apply_readme(once, S, "main")
assert once == twice, "apply_readme must be idempotent"
assert "assets/banner.svg" not in once and "# Demo" in once and once.count(b.H_START) == 1 and once.count(b.F_START) == 1
assert "# Demo Repo" in b.apply_readme("", S, "main"), "empty README gets a title"
assert "logo.png" in b.apply_readme('<img src="logo.png" />\n# X\n', S, "main"), "non-hero images are kept"
xml.dom.minidom.parseString(b.banner_svg(S))  # well-formed SVG
print("ok")
