#!/usr/bin/env bash
set -Eeuo pipefail
OUT_DIR="${OUT_DIR:-$HOME/UNIBOT_reports}"
python3 tools/compute_metrics.py
cp "$OUT_DIR/REPORT.md" docs/REPORT.md || true
echo "Report generated: $OUT_DIR/REPORT.md and docs/REPORT.md"
