#!/usr/bin/env bash
set -euo pipefail
queue_dir="$(pwd)/.state/queued_patches"
[ -d "$queue_dir" ] || { echo "No queued_patches at $queue_dir"; exit 1; }
echo "Queued patches:"; ls -1 "$queue_dir" || true
echo
read -r -p "Enter filename to review/apply (empty to exit): " pick
[ -n "${pick:-}" ] || { echo "No selection."; exit 0; }
patchpath="$queue_dir/$pick"
[ -f "$patchpath" ] || { echo "Not found: $patchpath" >&2; exit 2; }
echo; echo "---- patch preview ----"
sed -n '1,200p' "$patchpath" || true
echo "-----------------------"; echo
read -r -p "Apply this patch and commit? type 'yes': " confirm
[ "$confirm" = "yes" ] || { echo "Aborted."; exit 0; }

# Create a safe branch for applying the queued patch
timestamp() { date -u +"%Y%m%dT%H%M%SZ"; }
base="$(basename "$patchpath")"
safe_branch="queued-patch/$(timestamp)-${base//[^A-Za-z0-9._-]/-}"

echo "Creating branch: $safe_branch"
git fetch --quiet || true
git checkout -b "$safe_branch"

echo "Checking patch applies cleanly..."
git apply --check "$patchpath"
echo "Applying patch into index..."
git apply --index "$patchpath"
commit_msg="Apply queued patch: $base"
git commit -m "$commit_msg"

echo "Patch applied and committed on branch: $safe_branch"
echo "To push: git push -u origin $safe_branch"
