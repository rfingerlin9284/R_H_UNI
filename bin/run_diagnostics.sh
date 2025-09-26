#!/bin/bash

# This script verifies the environment, configurations, and core modules.
# It generates a diagnostics report in artifacts/<run_id>/reports/diagnostics.json.

set -e

# Define the root directory and artifacts directory
ROOT_DIR="$(dirname $(dirname $(realpath $0)))"
ARTIFACTS_DIR="$ROOT_DIR/artifacts"
RUN_ID=$(date +%Y%m%d_%H%M%S)
REPORT_DIR="$ARTIFACTS_DIR/$RUN_ID/reports"

# Create necessary directories
mkdir -p "$REPORT_DIR"

# Diagnostics checks
PYTHON_VERSION=$(python3 --version 2>&1 || echo "Python not found")
PIP_VERSION=$(pip --version 2>&1 || echo "Pip not found")
REQUIRED_MODULES=(numpy pandas)

# Check Python modules
MODULE_STATUS=()
for MODULE in "${REQUIRED_MODULES[@]}"; do
  if python3 -c "import $MODULE" 2>/dev/null; then
    MODULE_STATUS+=("$MODULE: OK")
  else
    MODULE_STATUS+=("$MODULE: MISSING")
  fi
done

# Write diagnostics report
cat << EOF > "$REPORT_DIR/diagnostics.json"
{
  "python_version": "$PYTHON_VERSION",
  "pip_version": "$PIP_VERSION",
  "module_status": {
    $(printf '"%s": "%s",
' "${MODULE_STATUS[@]}" | sed '$ s/,$//')
  }
}
EOF

# Print success message
echo "Diagnostics completed. Report generated at $REPORT_DIR/diagnostics.json."