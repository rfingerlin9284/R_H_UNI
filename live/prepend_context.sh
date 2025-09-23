#!/usr/bin/env bash
#
# live/prepend_context.sh - header snippet for live/ artifacts
set -euo pipefail

prepend_header() {
  cat <<'HEADER'
# Live environment artifact header (R_U_UNI)
# Mark files intended for live usage.
HEADER
}

export -f prepend_header
