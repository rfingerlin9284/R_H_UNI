#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd "$(dirname "$0")/.." && pwd)"
out_dir="$HOME/Desktop/wolf_packs"
mkdir -p "$out_dir"
echo "Copying wolf_packs templates to $out_dir"
rsync -a --exclude='__pycache__' "$repo_root/wolf_packs/" "$out_dir/"
echo "Done. Open $out_dir in your editor to review the assembled templates."
