from __future__ import annotations

import struct
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def png_dimensions(path: Path) -> tuple[int, int]:
    signature = path.read_bytes()[:24]
    assert signature[:8] == b"\x89PNG\r\n\x1a\n"
    return struct.unpack(">II", signature[16:24])


class ProfessionalIdentitySurfaceTests(unittest.TestCase):
    def test_new_icon_is_square_and_high_resolution(self) -> None:
        icon = ROOT / "JC-favicon.png"
        self.assertEqual(png_dimensions(icon), (512, 512))

    def test_social_preview_is_declared_and_has_standard_dimensions(self) -> None:
        card = ROOT / "assets" / "og-card.png"
        head = (ROOT / "_includes" / "head-custom.html").read_text(encoding="utf-8")
        self.assertEqual(png_dimensions(card), (1200, 630))
        self.assertIn('property="og:image"', head)
        self.assertIn('name="twitter:card"', head)

    def test_header_uses_semantic_navigation_and_home_removes_duplicate_profile_link(self) -> None:
        layout = (ROOT / "_layouts" / "template.html").read_text(encoding="utf-8")
        home = (ROOT / "index.md").read_text(encoding="utf-8")
        self.assertIn('<nav class="site-nav" aria-label="Primary">', layout)
        self.assertNotIn('[ACADEMIA]', home)


if __name__ == "__main__":
    unittest.main()
