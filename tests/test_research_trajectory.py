from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ResearchTrajectoryTests(unittest.TestCase):
    def test_consolidated_research_page_contains_lines_and_selected_contributions(self) -> None:
        page = (ROOT / "Research.md").read_text(encoding="utf-8")
        for section in ("## Research Lines", "## Research Trajectory"):
            self.assertIn(section, page)
        expected_dois = (
            "10.1016/j.lwt.2015.06.044",
            "10.1016/j.jfoodeng.2014.09.028",
            "10.3390/antiox8090360",
            "10.1016/j.ifset.2020.102442",
            "10.1016/j.lwt.2019.108809",
        )
        for doi in expected_dois:
            self.assertIn(doi, page)
        self.assertIn("first six-year research evaluation period", page)

    def test_featured_contributions_exist_in_the_publications_catalogue(self) -> None:
        page = (ROOT / "Research.md").read_text(encoding="utf-8")
        catalogue = json.loads((ROOT / "_data" / "publications.json").read_text(encoding="utf-8"))
        catalogue_dois = {item["doi"] for item in catalogue}
        featured = {
            "https://doi.org/10.1016/j.lwt.2015.06.044",
            "https://doi.org/10.1016/j.jfoodeng.2014.09.028",
            "https://doi.org/10.3390/antiox8090360",
            "https://doi.org/10.1016/j.ifset.2020.102442",
            "https://doi.org/10.1016/j.lwt.2019.108809",
        }
        self.assertTrue(featured.issubset(catalogue_dois))
        for doi in featured:
            self.assertIn(doi, page)

    def test_navigation_and_legacy_pages_point_to_the_canonical_research_page(self) -> None:
        layout = (ROOT / "_layouts" / "template.html").read_text(encoding="utf-8")
        home = (ROOT / "index.md").read_text(encoding="utf-8")
        legacy_lines = (ROOT / "ResearchLines.md").read_text(encoding="utf-8")
        legacy_trajectory = (ROOT / "ResearchTrajectory.md").read_text(encoding="utf-8")
        self.assertIn("'/Research'", layout)
        self.assertIn("Research</a>", layout)
        self.assertIn("'/Research'", home)
        self.assertIn("'/Research'", legacy_lines)
        self.assertIn("'/Research'", legacy_trajectory)


if __name__ == "__main__":
    unittest.main()
