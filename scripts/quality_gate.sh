#!/usr/bin/env bash

set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

VENV="$ROOT/.venv/bin"

echo "=================================="
echo "       QUALITY GATE"
echo "=================================="

echo ""
echo "[1/4] Ruff: lint"
"$VENV/ruff" check app tests

echo ""
echo "[2/4] Ruff: format"
"$VENV/ruff" format --check app tests

echo ""
echo "[3/4] BasedPyright: type checking"
"$VENV/basedpyright" app tests

echo ""
echo "[4/4] Pytest: tests and coverage"
"$VENV/pytest" -v \
    --cov=app \
    --cov-report=term-missing \
    --cov-fail-under=100

echo ""
echo "=================================="
echo " QUALITY GATE PASSED"
echo "=================================="
