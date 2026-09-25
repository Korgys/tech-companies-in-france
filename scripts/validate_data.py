#!/usr/bin/env python3
"""Validate the departmental CSV files."""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
import unicodedata
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit


EXPECTED_HEADER = [
    "name",
    "domain",
    "city",
    "website",
    "careers_url",
    "linkedin_url",
    "known_stack",
    "company_size",
    "notes",
    "last_verified",
]
ALLOWED_DOMAINS = {
    "adtech",
    "agency",
    "agtech",
    "ai",
    "banking",
    "cybersecurity",
    "data",
    "deeptech",
    "digital",
    "ecommerce",
    "edtech",
    "energy",
    "enterprise",
    "fintech",
    "gaming",
    "healthtech",
    "industrial",
    "insurance",
    "it-services",
    "public-sector",
    "robotics",
    "saas",
    "software",
    "studio",
    "telecom",
    "transport",
}
ALLOWED_COMPANY_SIZES = {"", "1-10", "11-50", "51-1000", "1000+"}
MULTI_VALUE_FIELDS = {"domain", "known_stack"}
REQUIRED_FIELDS = {"name", "domain", "city"}
URL_FIELDS = {"website", "careers_url", "linkedin_url"}


@dataclass
class ValidationResult:
    paths: list[Path]
    total: int = 0
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def sort_value(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value.casefold())
    return "".join(char for char in normalized if not unicodedata.combining(char))


def row_sort_key(row: list[str]) -> tuple[object, ...]:
    name = row[EXPECTED_HEADER.index("name")]
    city = row[EXPECTED_HEADER.index("city")]
    return sort_value(name), sort_value(city), name, city, tuple(row)


def is_valid_url(value: str) -> bool:
    if any(char.isspace() for char in value):
        return False
    try:
        parsed = urlsplit(value)
        return parsed.scheme in {"http", "https"} and bool(parsed.hostname)
    except ValueError:
        return False


def validate_data(data_dir: Path) -> ValidationResult:
    paths = sorted(data_dir.rglob("*.csv"))
    result = ValidationResult(paths=paths)
    duplicate_locations: dict[tuple[str, str], list[str]] = defaultdict(list)

    if not paths:
        result.errors.append(f"{data_dir}: aucun fichier CSV")
        return result

    indexes = {field: EXPECTED_HEADER.index(field) for field in EXPECTED_HEADER}
    for path in paths:
        try:
            with path.open(encoding="utf-8-sig", newline="") as stream:
                reader = csv.reader(stream, strict=True)
                if next(reader, None) != EXPECTED_HEADER:
                    result.errors.append(f"{path}: en-tête incorrect")
                    continue

                previous_row: list[str] | None = None
                for row in reader:
                    location = f"{path}:{reader.line_num}"
                    if len(row) != len(EXPECTED_HEADER):
                        result.errors.append(
                            f"{location}: {len(row)} colonnes au lieu de {len(EXPECTED_HEADER)}"
                        )
                        continue

                    if any(value.strip() for value in row):
                        result.total += 1
                        name = row[indexes["name"]]
                        city = row[indexes["city"]]
                        if previous_row is not None and row_sort_key(row) < row_sort_key(previous_row):
                            result.errors.append(
                                f"{location}: ligne non triée ({name!r}, {city!r})"
                            )
                        previous_row = row
                        duplicate_locations[(sort_value(name), sort_value(city))].append(location)

                    for field_name, value in zip(EXPECTED_HEADER, row):
                        if value != value.strip():
                            result.errors.append(
                                f"{location}: {field_name} contient des espaces superflus"
                            )
                        if field_name in REQUIRED_FIELDS and not value:
                            result.errors.append(f"{location}: {field_name} est vide")
                        if field_name in URL_FIELDS and value and not is_valid_url(value):
                            result.errors.append(f"{location}: {field_name} n'est pas une URL HTTP(S) valide")
                        if field_name in MULTI_VALUE_FIELDS and value:
                            if "," in value or ";" in value:
                                result.errors.append(
                                    f"{location}: {field_name} doit utiliser | comme séparateur"
                                )
                            values = value.split("|")
                            if any(not item or item != item.strip() for item in values):
                                result.errors.append(
                                    f"{location}: {field_name} contient un séparateur ou des espaces invalides"
                                )
                            if len(values) != len(set(values)):
                                result.errors.append(
                                    f"{location}: {field_name} contient une valeur dupliquée"
                                )

                    domains = row[indexes["domain"]].split("|") if row[indexes["domain"]] else []
                    invalid_domains = sorted(set(domains) - ALLOWED_DOMAINS)
                    if invalid_domains:
                        result.errors.append(
                            f"{location}: domain non autorisé : {', '.join(invalid_domains)}"
                        )

                    company_size = row[indexes["company_size"]]
                    if company_size not in ALLOWED_COMPANY_SIZES:
                        result.errors.append(
                            f"{location}: company_size non autorisé : {company_size!r}"
                        )

                    verified = row[indexes["last_verified"]]
                    if verified:
                        try:
                            if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", verified):
                                raise ValueError
                            date.fromisoformat(verified)
                        except ValueError:
                            result.errors.append(
                                f"{location}: last_verified doit être une date YYYY-MM-DD valide"
                            )
        except (OSError, UnicodeError, csv.Error) as exc:
            result.errors.append(f"{path}: CSV illisible : {exc}")

    for (name, city), locations in sorted(duplicate_locations.items()):
        if name and city and len(locations) > 1:
            result.warnings.append(
                f"doublon potentiel pour {name!r} à {city!r} : {', '.join(locations)}"
            )

    return result


def update_readme(readme: Path, total: int) -> None:
    content = readme.read_text(encoding="utf-8")
    badge = (
        "<!-- company-count:start -->\n"
        f"[![Implantations tech : {total}](https://img.shields.io/badge/"
        f"implantations_tech-{total}-059669?style=for-the-badge&logo=databricks&logoColor=white)](data/)\n"
        "<!-- company-count:end -->"
    )
    content, replacements = re.subn(
        r"<!-- company-count:start -->.*?<!-- company-count:end -->",
        lambda match: badge,
        content,
        flags=re.DOTALL,
    )
    if replacements != 1:
        raise ValueError("README.md : bloc company-count absent ou dupliqué")
    readme.write_text(content, encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--update-readme", action="store_true")
    parser.add_argument("--readme", type=Path, default=Path("README.md"))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = validate_data(args.data_dir)
    if result.warnings:
        print("\n".join(f"Avertissement : {warning}" for warning in result.warnings), file=sys.stderr)
    if result.errors:
        print("\n".join(result.errors), file=sys.stderr)
        return 1

    print(f"Validation réussie : {len(result.paths)} fichier(s) CSV.")
    print(f"Implantations tech renseignées : {result.total}.")

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with Path(summary_path).open("a", encoding="utf-8") as summary:
            summary.write(
                f"### {result.total} implantations tech renseignées\n\n"
                f"{len(result.paths)} fichiers CSV validés.\n"
            )

    if args.update_readme:
        try:
            update_readme(args.readme, result.total)
        except (OSError, UnicodeError, ValueError) as exc:
            print(exc, file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
