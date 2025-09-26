#!/usr/bin/env bash
set -Eeuo pipefail
# Minimal GS harness: run pytest for wolf_packs and produce JSON artifacts
OUT_DIR="${OUT_DIR:-$HOME/UNIBOT_reports}"
mkdir -p "$OUT_DIR"
JUNIT_XML="$OUT_DIR/gs_junit.xml"
JSON_OUT="$OUT_DIR/gs_test_matrix.json"
SUMMARY_OUT="$OUT_DIR/run_summary.json"

echo "Running GS battery: pytest tests/wolf_packs -> $OUT_DIR"

# Run pytest and produce junit xml
if command -v pytest >/dev/null 2>&1; then
  pytest -q tests/wolf_packs --junit-xml="$JUNIT_XML"
  PYTHONPATH="$(pwd)" python3 scripts/gs_runner.py --junit "$JUNIT_XML" --out "$OUT_DIR"
  echo "GS artifacts written to: $OUT_DIR"
  exit 0
else
  echo "pytest not found. Install test deps first: python3 -m pip install -r requirements.txt" >&2
  exit 127
fi
