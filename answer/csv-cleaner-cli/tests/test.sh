#!/usr/bin/env sh
# 遇到错误立即停止
set -eu

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

python "$ROOT_DIR/tests/test_logic.py"
