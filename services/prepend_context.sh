#!/usr/bin/env bash
#
# services/prepend_context.sh - header helper for service-generated files
set -euo pipefail

prepend_header() {
  cat <<'HEADER'
# Services-generated artifact (R_U_UNI)
# Annotates files produced by services/ components.
HEADER
}

export -f prepend_header
