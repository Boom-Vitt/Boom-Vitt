"""Offline checks: python3 tools/brand/test_bbn_brand.py."""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

import bbn_brand as b

S = {"name": "demo", "title": "Demo Repo", "tagline_th": "ทดสอบ", "tagline_en": "test", "category": "web", "chips": ["A", "B"]}

class BrandTests(unittest.TestCase):
    def test_rewrite_is_idempotent(self):
        once = b.apply_readme('<img src="assets/banner.svg" alt="x" />\n\n# Demo\n\nbody\n', S, "main")
        self.assertEqual(once, b.apply_readme(once, S, "main"))
        self.assertNotIn("assets/banner.svg", once)
        self.assertIn("# Demo\n\nbody", once)
        for marker in (b.H_START, b.H_END, b.F_START, b.F_END):
            self.assertEqual(once.count(marker), 1)

    def test_old_blocks_are_replaced_and_body_is_preserved(self):
        body = '# Demo\n\n![Demo](docs/demo.png)\n\n```sh\nrun --example\n```\n\n[License](LICENSE)'
        old = f'{b.H_START}\nold badges\n{b.H_END}\n\n{body}\n\n{b.F_START}\nold promotions\n{b.F_END}\n'
        self.assertEqual(b.apply_readme(old, S, "main"), b.header(S, "main") + "\n" + body + "\n\n" + b.FOOTER)

    def test_empty_readme_gets_a_title(self):
        self.assertIn("# Demo Repo", b.apply_readme("", S, "main"))

    def test_non_hero_images_are_kept(self):
        self.assertIn('src="logo.png"', b.apply_readme('<img src="logo.png" />\n# X\n', S, "main"))

    def test_header_is_banner_only(self):
        header = b.header(S, "main")
        self.assertEqual(header.count("<img "), 1)
        self.assertIn('src=".github/brand/banner.svg"', header)
        self.assertNotIn("shields.io", header)
        self.assertNotIn("<a ", header)

    def test_footer_is_one_attribution_link(self):
        self.assertEqual(b.FOOTER, f'{b.F_START}\n[Made by BoomBigNose](https://github.com/Boom-Vitt)\n{b.F_END}\n')

    def test_banner_is_static_product_identity(self):
        svg = b.banner_svg(S)
        root = ET.fromstring(svg)
        texts = [''.join(e.itertext()) for e in root.findall('{http://www.w3.org/2000/svg}text')]
        for value in [S['title'], S['tagline_th'], S['tagline_en'], 'WEB', *S['chips']]:
            self.assertIn(value, texts)
        for forbidden in ('<image', 'base64', 'animation', '@keyframes', 'BOOMBIGNOSE ·'):
            self.assertNotIn(forbidden, svg)
        self.assertIn(b.CATS['web'][0], svg)

    def test_svg_and_header_escape_text(self):
        s = dict(S, title='A < B & "C"', tagline_th='ทดสอบ < & >', tagline_en='Use "A" & B', chips=['<chip>'])
        root = ET.fromstring(b.banner_svg(s))
        texts = [''.join(e.itertext()) for e in root.findall('{http://www.w3.org/2000/svg}text')]
        for value in (s['title'], s['tagline_th'], s['tagline_en'], '<chip>'):
            self.assertIn(value, texts)
        self.assertIn('&quot;C&quot;', b.header(s, 'main'))

    def test_cli_preserves_readme_filename_and_reruns(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            spec = root / 'spec.json'
            spec.write_text(json.dumps([S]), encoding='utf-8')
            repo = root / 'repo'
            repo.mkdir()
            readme = repo / 'Readme.md'
            readme.write_text('# Existing\n\nKeep this.\n', encoding='utf-8')
            command = [sys.executable, str(pathlib.Path(b.__file__)), str(spec), 'demo', str(repo)]
            subprocess.run(command, check=True, capture_output=True)
            first = readme.read_bytes(), (repo / '.github/brand/banner.svg').read_bytes()
            subprocess.run(command, check=True, capture_output=True)
            self.assertEqual(first, (readme.read_bytes(), (repo / '.github/brand/banner.svg').read_bytes()))
            self.assertNotIn('README.md', [p.name for p in repo.iterdir()])
            self.assertIn('Keep this.', readme.read_text())


if __name__ == '__main__':
    unittest.main(verbosity=2)
