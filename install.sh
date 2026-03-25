#!/usr/bin/env bash
set -euo pipefail

APPIMAGE_DEFAULT="apic-1-linux-x86_64.AppImage"
APPIMAGE_SOURCE="${1:-$APPIMAGE_DEFAULT}"

if [[ ! -f "$APPIMAGE_SOURCE" ]]; then
  echo "Error: AppImage not found: $APPIMAGE_SOURCE"
  echo "Usage: ./setup.sh [path-to-appimage]"
  exit 1
fi

BIN_DIR="$HOME/.local/bin"
TARGET_VERSIONED="$BIN_DIR/apic-1"
TARGET_LINK="$BIN_DIR/apic"
SHELL_RC=""

mkdir -p "$BIN_DIR"

cp "$APPIMAGE_SOURCE" "$TARGET_VERSIONED"
chmod +x "$TARGET_VERSIONED"
ln -sfn "$TARGET_VERSIONED" "$TARGET_LINK"

# Detect shell rc file
if [[ "${SHELL:-}" == *"zsh" ]]; then
  SHELL_RC="$HOME/.zshrc"
else
  SHELL_RC="$HOME/.bashrc"
fi

# Add ~/.local/bin to PATH if missing
if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$SHELL_RC" 2>/dev/null; then
  echo '' >> "$SHELL_RC"
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
  echo "Added ~/.local/bin to PATH in $SHELL_RC"
fi

echo "Installed:"
echo "  $TARGET_VERSIONED"
echo "  $TARGET_LINK -> $TARGET_VERSIONED"
echo
echo "Open a new terminal, or run:"
echo "  export PATH=\"$HOME/.local/bin:\$PATH\""
echo
echo "Then test:"
echo "  apic --help"
