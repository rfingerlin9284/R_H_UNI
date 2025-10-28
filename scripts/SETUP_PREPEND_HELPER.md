# Setup Instructions for Prepend Helper Script

This guide provides specific prompt commands for VSCode agents to set up the prepend helper script in any repository.

## Generic Script (Auto-detects Repository Name)

The `prepend_context.sh` script now auto-detects the repository name from git or the current directory, making it work across multiple repositories without modification.

---

## Setup Prompts for VSCode Agents

### For "rick live clean" Repository:

```
Create a scripts directory in the root of the repository and add a file named scripts/prepend_context.sh with the following content:

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

Make the script executable by running: chmod +x scripts/prepend_context.sh
```

---

### For "rick live prototype" Repository:

```
Create a scripts directory in the root of the repository and add a file named scripts/prepend_context.sh with the following content:

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

Make the script executable by running: chmod +x scripts/prepend_context.sh
```

---

## Usage Examples

Once set up, the script can be used the same way in all repositories:

```bash
# Source the script
source scripts/prepend_context.sh

# Call the function - it will automatically use the correct repo name
prepend_header
```

### Example Outputs:

- In R_H_UNI repo: `# R_H_UNI - generated 2025-10-28T23:24:00Z`
- In rick-live-clean repo: `# rick-live-clean - generated 2025-10-28T23:24:00Z`
- In rick-live-prototype repo: `# rick-live-prototype - generated 2025-10-28T23:24:00Z`

### Override Repository Name (Optional):

If you need to override the auto-detected name:

```bash
REPO_NAME="custom-name" prepend_header
# Output: # custom-name - generated 2025-10-28T23:24:00Z
```

---

## Features

- **Auto-detection**: Automatically detects repository name from git or directory name
- **Cross-repository**: Same script works in all repositories without modification
- **Override support**: Can be overridden with REPO_NAME environment variable
- **Zero configuration**: Just copy the script and it works
- **Consistent format**: Generates standardized headers across all repositories

---

## Quick Copy Command

For quick setup in any repository, you can copy the script from R_H_UNI:

```bash
# From within the target repository
mkdir -p scripts
cp /path/to/R_H_UNI/scripts/prepend_context.sh scripts/
chmod +x scripts/prepend_context.sh
```
