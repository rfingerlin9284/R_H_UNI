#!/usr/bin/env bash
set -euo pipefail

# Define directories and files
TEST_DIR="tests/wolf_packs"
REPORT_DIR="artifacts/$(date +%Y%m%d_%H%M%S)/reports"
LOG_FILE="$REPORT_DIR/gs_test_log.txt"

# Create report directory
mkdir -p "$REPORT_DIR"

# Run tests
pytest "$TEST_DIR" --junitxml="$REPORT_DIR/gs_junit.xml" | tee "$LOG_FILE"

# Check test results
if grep -q "failed" "$LOG_FILE"; then
  echo "❌ Some tests failed. Check the report at $LOG_FILE"
  exit 1
else
  echo "✅ All tests passed. Report available at $LOG_FILE"
fi

# Toggle live readiness
LIVE_READY_FILE=".live_ready"
if [ -f "$LIVE_READY_FILE" ]; then
  echo "Toggling live readiness..."
  rm "$LIVE_READY_FILE"
  echo "Live readiness disabled."
else
  touch "$LIVE_READY_FILE"
  echo "Live readiness enabled."
fi