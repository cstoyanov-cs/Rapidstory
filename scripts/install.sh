#!/usr/bin/env bash
# =============================================================================
# RapidStory – Smart install / reinstall script
# Place in scripts/install.sh
# Run anytime after code changes → everything is updated instantly
# =============================================================================

set -euo pipefail

# Chemin absolu de la racine du projet
SCRIPT_PATH="${BASH_SOURCE[0]}"
PROJECT_DIR="$(cd "$(dirname "$SCRIPT_PATH")/.." && pwd)"
BIN_NAME="rapidstory"

echo "RapidStory – Smart installer / updater"
echo "============================================"

# 1. Ensure ~/.local/bin is in PATH
if ! grep -q '\.local/bin' "$HOME/.bashrc" 2>/dev/null; then
  echo "Adding ~/.local/bin to PATH in ~/.bashrc"
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
  export PATH="$HOME/.local/bin:$PATH"
fi

# 2. Install / reinstall
echo "Installing/updating RapidStory with pipx (editable mode)..."
if pipx list --short | grep -q "^$BIN_NAME "; then
  echo "RapidStory already installed → reinstalling..."
  pipx uninstall "$BIN_NAME" << EOF
y
EOF
  pipx install --editable "$PROJECT_DIR"
else
  echo "First installation..."
  pipx install --editable "$PROJECT_DIR"
fi

# 3. Final check
if command -v "$BIN_NAME" >/dev/null; then
  echo ""
  echo "SUCCESS! RapidStory is up-to-date."
  echo "Ctrl+R and Ctrl+Up are ready to use."
  echo ""
  echo "Tip: run ./scripts/install.sh after any code change"
else
  echo "ERROR: $BIN_NAME not found in PATH"
  exit 1
fi

echo "All done !"
