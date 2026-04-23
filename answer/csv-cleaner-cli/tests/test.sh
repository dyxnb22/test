#!/usr/bin/env sh
set -eu

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

python "$ROOT_DIR/tests/test_logic.py"
