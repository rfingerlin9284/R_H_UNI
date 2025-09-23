#!/usr/bin/env bash
#
# runtime/prepend_context.sh - runtime-facing prepend header helper
set -euo pipefail

prepend_header() {
  cat <<'HEADER'
# R_U_UNI runtime header
# Managed by dev tooling — used to annotate generated runtime artifacts.
HEADER
}

export -f prepend_header
