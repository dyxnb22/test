#!/usr/bin/env python3
import csv
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    input_file = root / "environment" / "dirty_data.csv"
    output_file = root / "solution" / "cleaned_data.csv"

    if not output_file.exists():
        print("FAIL: cleaned_data.csv was not generated")
        return 1

    rows = read_csv(output_file)
    expected = [
        {
            "id": "1",
            "name": "Alice Smith",
            "email": "alice@example.com",
            "age": "30",
            "score": "88.46",
        },
        {
            "id": "4",
            "name": "Dora",
            "email": "dora@example.com",
            "age": "",
            "score": "",
        },
        {
            "id": "5",
            "name": "Frank",
            "email": "frank@example.com",
            "age": "",
            "score": "60.10",
        },
        {
            "id": "6",
            "name": "Grace Hopper",
            "email": "grace@example.com",
            "age": "85",
            "score": "100.00",
        },
    ]

    if rows != expected:
        print("FAIL: cleaned output mismatch")
        print("Expected:", expected)
        print("Actual:", rows)
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
