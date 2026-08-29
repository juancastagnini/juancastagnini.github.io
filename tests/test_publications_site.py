from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "_data" / "publications.json"
INCLUDE_FILE = ROOT / "_includes" / "publication-list.html"
SCRIPT_FILE = ROOT / "assets" / "js" / "publications-filter.js"


def load_publications() -> list[dict]:
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


class PublicationsSiteTests(unittest.TestCase):
    def test_publications_data_includes_existing_and_latest_records(self) -> None:
        publications = load_publications()
        dois = {publication["doi"] for publication in publications}

        self.assertEqual(len(publications), 98)
        self.assertIn("https://doi.org/10.1016/j.foodchem.2024.142283", dois)
        self.assertIn("https://doi.org/10.1007/s00217-026-05248-9", dois)
        self.assertIn("https://doi.org/10.1007/s00216-025-06073-x", dois)
        self.assertIn("https://doi.org/10.33255/2957/320", dois)
        self.assertNotIn("https://doi.org/10.1007/s44187-026-01152-z", dois)
        self.assertEqual(publications[0]["year"], 2026)
        self.assertEqual(
            [publication["published_date"] for publication in publications],
            sorted(
                (publication["published_date"] for publication in publications), reverse=True
            ),
        )

    def test_every_publication_declares_a_safe_access_route(self) -> None:
        allowed_routes = {
            "publisher-oa",
            "free-to-read-rights-unverified",
            "repository-full-text",
            "publisher-only",
            "rights-under-review",
        }

        for publication in load_publications():
            self.assertTrue(
                {"year", "citation", "doi", "access_route", "access_label"}
                <= publication.keys()
            )
            self.assertIn(publication["access_route"], allowed_routes)
            self.assertTrue(publication["doi"].startswith("https://doi.org/"))
            self.assertNotIn("<", publication["citation"])
            self.assertNotIn("&amp;", publication["citation"])
            if publication["access_route"] == "publisher-oa":
                self.assertTrue(publication.get("fulltext_url"))
                self.assertTrue(publication.get("license"))
                self.assertTrue(publication.get("rights_evidence_url"))

    def test_verified_2026_publisher_routes_have_licences(self) -> None:
        expected_licenses = {
            "https://doi.org/10.1016/j.ijfoodmicro.2025.111436": "CC BY 4.0",
            "https://doi.org/10.1016/j.ifset.2026.104445": "CC BY-NC-ND 4.0",
            "https://doi.org/10.1016/j.fbio.2026.108313": "CC BY-NC 4.0",
            "https://doi.org/10.1007/s00216-025-06073-x": "CC BY 4.0",
        }
        by_doi = {publication["doi"]: publication for publication in load_publications()}

        for doi, license_name in expected_licenses.items():
            publication = by_doi[doi]
            self.assertEqual(publication["access_route"], "publisher-oa")
            self.assertEqual(publication["license"], license_name)
            self.assertEqual(publication["fulltext_url"], doi)
            self.assertEqual(publication["rights_evidence_url"], doi)

    def test_verified_2025_publisher_routes_have_licences(self) -> None:
        expected_licenses = {
            "https://doi.org/10.3390/molecules30173589": "CC BY 4.0",
            "https://doi.org/10.3390/foods14223908": "CC BY 4.0",
            "https://doi.org/10.3390/foods14152583": "CC BY 4.0",
            "https://doi.org/10.3390/biology14070889": "CC BY 4.0",
            "https://doi.org/10.12873/452rodriguez": "CC BY-NC-ND 4.0",
            "https://doi.org/10.1080/19476337.2025.2549373": "CC BY 4.0",
            "https://doi.org/10.1016/j.jafr.2025.101666": "CC BY-NC-ND 4.0",
            "https://doi.org/10.1016/j.foodchem.2025.146367": "CC BY 4.0",
            "https://doi.org/10.1016/j.foodchem.2025.143085": "CC BY 4.0",
            "https://doi.org/10.1016/j.cofs.2025.101365": "CC BY-NC 4.0",
            "https://doi.org/10.1016/j.afres.2025.100963": "CC BY 4.0",
            "https://doi.org/10.1007/s11947-025-03897-4": "CC BY 4.0",
            "https://doi.org/10.1007/s11947-025-03751-7": "CC BY 4.0",
            "https://doi.org/10.1007/s11947-024-03553-3": "CC BY 4.0",
        }
        by_doi = {publication["doi"]: publication for publication in load_publications()}

        for doi, license_name in expected_licenses.items():
            publication = by_doi[doi]
            self.assertEqual(publication["access_route"], "publisher-oa")
            self.assertEqual(publication["license"], license_name)
            self.assertEqual(publication["fulltext_url"], doi)
            self.assertEqual(publication["rights_evidence_url"], doi)

    def test_publications_page_uses_static_accessible_components(self) -> None:
        self.assertTrue(INCLUDE_FILE.exists())
        self.assertTrue(SCRIPT_FILE.exists())

        include = INCLUDE_FILE.read_text(encoding="utf-8")
        script = SCRIPT_FILE.read_text(encoding="utf-8")

        self.assertIn("site.data.publications", include)
        self.assertIn('aria-live="polite"', include)
        self.assertIn("data-access", include)
        self.assertIn("hidden", script)
        self.assertIn("aria-pressed", script)


if __name__ == "__main__":
    unittest.main()
