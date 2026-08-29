from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class HomepageProfileTests(unittest.TestCase):
    def test_homepage_presents_current_research_profile_and_service(self) -> None:
        home = (ROOT / "index.md").read_text(encoding="utf-8")
        expected_sections = (
            "## Research Profile",
            "## Current Roles and Academic Service",
            "## Selected Academic Experience",
            "## Education",
        )
        for section in expected_sections:
            self.assertIn(section, home)
        self.assertIn("European Food Safety Authority (EFSA)", home)
        self.assertIn("Current Nutrition Reports", home)
        self.assertIn("Current Food Science and Technology Reports", home)

    def test_homepage_keeps_public_contact_surface_intentional(self) -> None:
        home = (ROOT / "index.md").read_text(encoding="utf-8")
        self.assertNotIn("juan@juancastagnini.eu", home)
        self.assertIn("ORCiD", home)


if __name__ == "__main__":
    unittest.main()
