#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path


def normalize_name(name: str) -> str:
    return " ".join(name.split()).title()


def email_valid(email: str) -> bool:
    if "@" not in email:
        return False
    local, domain = email.split("@", 1)
    return bool(local) and "." in domain


def parse_age(age_raw: str) -> str:
    try:
        age = int(age_raw)
    except ValueError:
        return ""
    return str(age) if 0 <= age <= 120 else ""


def parse_score(score_raw: str) -> str:
    try:
        score = float(score_raw)
    except ValueError:
        return ""
    if 0 <= score <= 100:
        return f"{score:.2f}"
    return ""


def clean_rows(input_path: Path):
    cleaned = []
    seen_ids = set()

    with input_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, skipinitialspace=True)
        if reader.fieldnames is None:
            return cleaned

        # Normalize header names from potentially dirty input.
        reader.fieldnames = [h.strip() for h in reader.fieldnames]

        for row in reader:
            if row is None:
                continue

            normalized = {k.strip(): (v.strip() if v is not None else "") for k, v in row.items()}

            if all(v == "" for v in normalized.values()):
                continue

            raw_id = normalized.get("id", "")
            try:
                row_id = int(raw_id)
                if row_id <= 0:
                    continue
            except ValueError:
                continue

            if row_id in seen_ids:
                continue

            email = normalized.get("email", "").lower()
            if not email_valid(email):
                continue

            cleaned.append(
                {
                    "id": str(row_id),
                    "name": normalize_name(normalized.get("name", "")),
                    "email": email,
                    "age": parse_age(normalized.get("age", "")),
                    "score": parse_score(normalized.get("score", "")),
                }
            )
            seen_ids.add(row_id)

    cleaned.sort(key=lambda item: int(item["id"]))
    return cleaned


def write_rows(rows, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "email", "age", "score"])
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean dirty CSV data")
    parser.add_argument("--input", required=True, help="Path to dirty CSV")
    parser.add_argument("--output", required=True, help="Path to cleaned CSV")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    rows = clean_rows(input_path)
    write_rows(rows, output_path)


if __name__ == "__main__":
    main()
