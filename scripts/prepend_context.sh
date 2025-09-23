#!/usr/bin/env bash
#
# prepend_context.sh - small reusable helper to emit a standard header/context
# Usage:
#   source scripts/prepend_context.sh
#   prepend_header > /path/to/generated_file
#
set -euo pipefail

prepend_header() {
  cat <<'HEADER'
# Project: R_U_UNI
# Generated file header — keep in sync across tools.
# DO NOT EDIT MANUALLY unless you are intentionally changing generation metadata.
HEADER
}

export -f prepend_header
