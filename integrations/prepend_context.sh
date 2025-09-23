#!/usr/bin/env bash
#
# integrations/prepend_context.sh - standard header for integration outputs
set -euo pipefail

prepend_header() {
  cat <<'HEADER'
# Integrations artifact header (R_U_UNI)
# Indicates integration-generated content and generation metadata spot.
HEADER
}

export -f prepend_header
