#!/usr/bin/env bash
#
# filters/prepend_context.sh - prepend helper for filter outputs
set -euo pipefail

prepend_header() {
  cat <<'HEADER'
# Filter output header (R_U_UNI)
# Use this to mark files produced by filters/.
HEADER
}

export -f prepend_header
