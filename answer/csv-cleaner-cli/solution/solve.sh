#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python "$ROOT_DIR/solution/cleaner.py" \
  --input "$ROOT_DIR/environment/dirty_data.csv" \
  --output "$ROOT_DIR/solution/cleaned_data.csv"
