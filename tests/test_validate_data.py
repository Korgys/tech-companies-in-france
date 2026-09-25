import csv
import tempfile
import unittest
from pathlib import Path

from scripts.validate_data import EXPECTED_HEADER, validate_data


VALID_ROW = {
    "name": "Alpha",
    "domain": "ai|software",
    "city": "Paris",
    "website": "https://example.com",
    "careers_url": "https://example.com/jobs",
    "linkedin_url": "https://www.linkedin.com/company/example",
    "known_stack": "Python|React",
    "company_size": "11-50",
    "notes": "Éditeur de logiciels",
    "last_verified": "2026-09-25",
}


class ValidateDataTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.data_dir = Path(self.temporary_directory.name) / "data"
        self.data_dir.mkdir()

    def tearDown(self):
        self.temporary_directory.cleanup()

    def write_csv(self, rows, header=EXPECTED_HEADER, name="75-paris.csv"):
        path = self.data_dir / name
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=header)
            writer.writeheader()
            writer.writerows(rows)
        return path

    def test_accepts_valid_row_and_blank_last_verified(self):
        row = VALID_ROW | {"last_verified": ""}
        self.write_csv([row])

        result = validate_data(self.data_dir)

        self.assertEqual([], result.errors)
        self.assertEqual(1, result.total)

    def test_rejects_missing_required_fields(self):
        self.write_csv([VALID_ROW | {"name": "", "domain": "", "city": ""}])

        result = validate_data(self.data_dir)

        self.assertIn("name est vide", "\n".join(result.errors))
        self.assertIn("domain est vide", "\n".join(result.errors))
        self.assertIn("city est vide", "\n".join(result.errors))

    def test_rejects_invalid_domain_size_urls_and_date(self):
        row = VALID_ROW | {
            "domain": "unknown",
            "company_size": "51-200",
            "website": "example.com",
            "careers_url": "ftp://example.com/jobs",
            "linkedin_url": "https://[invalid",
            "last_verified": "2026-02-30",
        }
        self.write_csv([row])

        errors = "\n".join(validate_data(self.data_dir).errors)

        self.assertIn("domain non autorisé", errors)
        self.assertIn("company_size non autorisé", errors)
        self.assertEqual(3, errors.count("URL HTTP(S) valide"))
        self.assertIn("last_verified doit être une date YYYY-MM-DD valide", errors)

    def test_rejects_bad_header_spacing_separator_and_sort_order(self):
        self.write_csv(
            [
                VALID_ROW | {"name": "Zulu", "domain": "ai,software"},
                VALID_ROW | {"name": " Alpha"},
            ]
        )

        errors = "\n".join(validate_data(self.data_dir).errors)

        self.assertIn("ligne non triée", errors)
        self.assertIn("name contient des espaces superflus", errors)
        self.assertIn("domain doit utiliser | comme séparateur", errors)

    def test_reports_potential_duplicate_without_failing(self):
        self.write_csv(
            [
                VALID_ROW,
                VALID_ROW | {"name": "Álpha", "city": "PARIS", "website": ""},
            ]
        )

        result = validate_data(self.data_dir)

        self.assertEqual([], result.errors)
        self.assertEqual(1, len(result.warnings))
        self.assertIn("doublon potentiel", result.warnings[0])


if __name__ == "__main__":
    unittest.main()
