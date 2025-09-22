#!/usr/bin/env bash
set -euo pipefail
timestamp(){ date -u +"%Y%m%dT%H%M%SZ"; }
[ "$#" -eq 1 ] || { echo "Usage: $0 \"short-title\"" >&2; exit 2; }
title="$1"
queue_dir="$(pwd)/.state/queued_patches"
mkdir -p "$queue_dir"
outfile="$queue_dir/$(timestamp)-$(echo "$title" | sed 's/[^A-Za-z0-9._-]/-/g').patch"
cat - > "$outfile"
echo "Patch queued: $outfile"
echo "To review/apply: bash scripts/ai_approval.sh"
