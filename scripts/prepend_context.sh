#!/usr/bin/env bash

# Generic prepend header function that auto-detects repository name
# Can be used across multiple repositories without modification
prepend_header() {
  local repo_name
  
  # Try to get repository name from git remote (if in a git repo)
  if git rev-parse --git-dir > /dev/null 2>&1; then
    repo_name=$(basename "$(git rev-parse --show-toplevel)" 2>/dev/null)
  fi
  
  # Fallback to directory name if git detection fails
  if [ -z "$repo_name" ]; then
    repo_name=$(basename "$(pwd)")
  fi
  
  # Allow override via environment variable
  repo_name="${REPO_NAME:-$repo_name}"
  
  echo "# ${repo_name} - generated $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}