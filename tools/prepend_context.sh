#!/usr/bin/env bash
#
# tools/prepend_context.sh - developer tools may source this to apply a uniform header
set -euo pipefail

prepend_header() {
  cat <<'HEADER'
# Tools-generated file (R_U_UNI)
# This header is inserted by tooling to document provenance.
HEADER
}

export -f prepend_header
