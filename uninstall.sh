#!/usr/bin/env bash
set -euo pipefail

BIN_DIR="$HOME/.local/bin"
TARGET_LINK="$BIN_DIR/apic"

echo "Removing apic command..."

if [[ -L "$TARGET_LINK" || -f "$TARGET_LINK" ]]; then
  rm -f "$TARGET_LINK"
  echo "Removed: $TARGET_LINK"
else
  echo "Not found: $TARGET_LINK"
fi

# Remove versioned binaries matching apic-* in ~/.local/bin (safe pattern)
shopt -s nullglob
versioned=( "$BIN_DIR"/apic-[0-9]* )
if (( ${#versioned[@]} > 0 )); then
  for f in "${versioned[@]}"; do
    rm -f "$f"
    echo "Removed: $f"
  done
else
  echo "No versioned apic binaries found in $BIN_DIR"
fi
shopt -u nullglob

echo
echo "Uninstall complete."
echo "Note: PATH line in your shell rc was not removed."
echo "If you want, remove this line manually from ~/.bashrc or ~/.zshrc:"
echo '  export PATH="$HOME/.local/bin:$PATH"'
