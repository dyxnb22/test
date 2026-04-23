#!/usr/bin/env sh
set -eu

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

python "$ROOT_DIR/solution/cleaner.py" \
  --input "$ROOT_DIR/environment/dirty_data.csv" \
  --output "$ROOT_DIR/solution/cleaned_data.csv"
