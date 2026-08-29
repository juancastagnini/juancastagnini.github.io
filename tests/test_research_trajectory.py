from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ResearchTrajectoryTests(unittest.TestCase):
    def test_page_contains_the_five_user_selected_six_year_contributions(self) -> None:
        page = (ROOT / "ResearchTrajectory.md").read_text(encoding="utf-8")
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

    def test_every_featured_contribution_links_to_a_catalogue_publication(self) -> None:
        page = (ROOT / "ResearchTrajectory.md").read_text(encoding="utf-8")
        catalogue = json.loads((ROOT / "_data" / "publications.json").read_text(encoding="utf-8"))
        catalogue_dois = {item["doi"] for item in catalogue}
        featured = (
            "https://doi.org/10.1016/j.lwt.2015.06.044",
            "https://doi.org/10.1016/j.jfoodeng.2014.09.028",
            "https://doi.org/10.3390/antiox8090360",
            "https://doi.org/10.1016/j.ifset.2020.102442",
            "https://doi.org/10.1016/j.lwt.2019.108809",
        )
        self.assertTrue(set(featured).issubset(catalogue_dois))
        for doi in featured:
            self.assertIn(doi, page)

    def test_homepage_surfaces_the_trajectory_page(self) -> None:
        home = (ROOT / "index.md").read_text(encoding="utf-8")
        self.assertIn("ResearchTrajectory", home)


if __name__ == "__main__":
    unittest.main()
