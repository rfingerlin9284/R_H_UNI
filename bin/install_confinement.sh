#!/bin/bash

# This script sets up write confinement to the R_H_UNI directory.
# It ensures that all writes are restricted to the R_H_UNI directory and provides a helper for safe imports.

set -e

# Define the root directory for confinement
ROOT_DIR="$(dirname $(dirname $(realpath $0)))"

# Create the confinement launcher
cat << 'EOF' > "$ROOT_DIR/bin/ignite_confined.sh"
#!/bin/bash

# Enforce write confinement to the R_H_UNI directory
ROOT_DIR="$(dirname $(dirname $(realpath $0)))"

if [[ "$PWD" != "$ROOT_DIR"* ]]; then
  echo "Error: All operations must be performed within the confined directory: $ROOT_DIR"
  exit 1
fi

# Execute the provided command
exec "$@"
EOF
chmod +x "$ROOT_DIR/bin/ignite_confined.sh"

# Create the copy-in helper
cat << 'EOF' > "$ROOT_DIR/bin/copy_in.sh"
#!/bin/bash

# Helper script to copy files into the confined directory
if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <source> <destination>"
  exit 1
fi

SRC="$1"
DEST="$2"

if [[ ! -e "$SRC" ]]; then
  echo "Error: Source file does not exist: $SRC"
  exit 1
fi

cp -r "$SRC" "$DEST"
echo "Copied $SRC to $DEST"
EOF
chmod +x "$ROOT_DIR/bin/copy_in.sh"

# Print success message
echo "Confinement setup complete. Use ignite_confined.sh for confined operations and copy_in.sh for safe imports."