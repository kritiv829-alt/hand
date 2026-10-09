"""Check a shortie links.json file for structural problems.

Usage:
    python src/scripts/validate_links.py [path/to/links.json]

Exits with status 1 and prints one line per problem if anything is wrong,
otherwise prints a short OK message.
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

DEFAULT_FILE = Path(__file__).resolve().parents[2] / "data" / "links.json"
CODE_PATTERN = re.compile(r"^[A-Za-z0-9]{4,12}$")
REQUIRED_FIELDS = ("url", "hits", "createdAt")


def is_valid_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def is_valid_timestamp(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def validate_record(code: str, record: object) -> list[str]:
    """Return a list of problems for one link entry. Empty means valid."""
    problems: list[str] = []
    if not CODE_PATTERN.match(code):
        problems.append(f"{code}: code must be 4-12 alphanumeric characters")
    if not isinstance(record, dict):
        problems.append(f"{code}: record must be an object")
        return problems

    for field in REQUIRED_FIELDS:
        if field not in record:
            problems.append(f"{code}: missing field '{field}'")

    if "url" in record and not is_valid_url(record["url"]):
        problems.append(f"{code}: url must be an http or https URL")
    if "hits" in record and (not isinstance(record["hits"], int) or record["hits"] < 0):
        problems.append(f"{code}: hits must be a non-negative integer")
    if "createdAt" in record and not is_valid_timestamp(record["createdAt"]):
        problems.append(f"{code}: createdAt must be an ISO 8601 timestamp")
    return problems


def validate_links(links: object) -> list[str]:
    """Validate the whole links mapping and return every problem found."""
    if not isinstance(links, dict):
        return ["top-level value must be an object keyed by short code"]
    problems: list[str] = []
    for code, record in links.items():
        problems.extend(validate_record(code, record))
    return problems


def load(path: Path) -> object:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def main(argv: list[str]) -> int:
    path = Path(argv[0]) if argv else DEFAULT_FILE
    if not path.exists():
        print(f"{path}: file not found")
        return 1
    try:
        links = load(path)
    except json.JSONDecodeError as err:
        print(f"{path}: invalid JSON ({err})")
        return 1

    problems = validate_links(links)
    if problems:
        print("\n".join(problems))
        return 1
    count = len(links)
    print(f"{path}: OK ({count} link{'s' if count != 1 else ''})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
