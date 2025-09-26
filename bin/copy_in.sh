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
