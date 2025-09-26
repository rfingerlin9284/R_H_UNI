#!/bin/bash

# Enforce write confinement to the R_H_UNI directory
ROOT_DIR="$(dirname $(dirname $(realpath $0)))"

if [[ "$PWD" != "$ROOT_DIR"* ]]; then
  echo "Error: All operations must be performed within the confined directory: $ROOT_DIR"
  exit 1
fi

# Execute the provided command
exec "$@"
