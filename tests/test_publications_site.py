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

    def test_known_closed_articles_do_not_advertise_full_text(self) -> None:
        closed_dois = {
            "https://doi.org/10.1016/j.foodchem.2025.145854",
            "https://doi.org/10.1007/s11130-025-01396-7",
        }
        by_doi = {publication["doi"]: publication for publication in load_publications()}

        for doi in closed_dois:
            publication = by_doi[doi]
            self.assertEqual(publication["access_route"], "publisher-only")
            self.assertEqual(
                publication["access_label"],
                "Publisher access — subscription may be required",
            )
            self.assertFalse(publication.get("fulltext_url"))

    def test_2024_rights_audit_distinguishes_oa_from_closed(self) -> None:
        by_doi = {publication["doi"]: publication for publication in load_publications()}
        audited_oa = {
            "https://doi.org/10.37349/eff.2024.00026",
            "https://doi.org/10.3390/plants13213079",
            "https://doi.org/10.3390/plants13192802",
            "https://doi.org/10.3390/plants13131795",
            "https://doi.org/10.3390/ijms252313202",
            "https://doi.org/10.3390/foods13203233",
            "https://doi.org/10.3390/foods13182943",
            "https://doi.org/10.3390/foods13121932",
            "https://doi.org/10.3390/antiox13121510",
            "https://doi.org/10.23938/assn.1089",
            "https://doi.org/10.14306/renhyd.28.4.2246",
            "https://doi.org/10.12873/444rodriguez",
            "https://doi.org/10.1016/j.tifs.2024.104619",
            "https://doi.org/10.1016/j.lwt.2024.117116",
            "https://doi.org/10.1016/j.ifset.2024.103590",
            "https://doi.org/10.1016/j.crfs.2024.100695",
        }
        for doi in audited_oa:
            self.assertEqual(by_doi[doi]["access_route"], "publisher-oa")
            self.assertTrue(by_doi[doi].get("license"))

        closed = by_doi["https://doi.org/10.1016/j.foodhyd.2023.109288"]
        self.assertEqual(closed["access_route"], "publisher-only")
        self.assertFalse(closed.get("fulltext_url"))

    def test_2023_rights_audit_distinguishes_oa_free_to_read_and_closed(self) -> None:
        by_doi = {publication["doi"]: publication for publication in load_publications()}
        audited_oa = {
            "https://doi.org/10.3390/plants12112211", "https://doi.org/10.3390/foods12224116",
            "https://doi.org/10.3390/foods12142717", "https://doi.org/10.3390/foods12030643",
            "https://doi.org/10.3390/antiox12122080", "https://doi.org/10.3390/antiox12020406",
            "https://doi.org/10.3390/antiox12010028", "https://doi.org/10.3390/agronomy13051397",
            "https://doi.org/10.3389/fsufs.2023.1217813", "https://doi.org/10.15586/qas.v15i2.1269",
            "https://doi.org/10.1016/j.trac.2023.117267", "https://doi.org/10.1016/j.lwt.2023.114898",
            "https://doi.org/10.1016/j.ifset.2022.103256", "https://doi.org/10.1016/j.foodchem.2023.136054",
            "https://doi.org/10.1016/j.foodchem.2022.134615",
        }
        for doi in audited_oa:
            self.assertEqual(by_doi[doi]["access_route"], "publisher-oa")
            self.assertTrue(by_doi[doi].get("license"))

        self.assertEqual(by_doi["https://doi.org/10.1111/ijfs.16457"]["access_route"], "free-to-read-rights-unverified")
        self.assertEqual(by_doi["https://doi.org/10.1016/j.foodhyd.2023.109057"]["access_route"], "publisher-only")

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
