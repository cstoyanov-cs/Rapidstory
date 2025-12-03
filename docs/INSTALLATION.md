```markdown
# RapidStory – Installation Guide

Ultra-fast Bash history search with a modern interface  
Replaces the classic `Ctrl+R` and ↑ key with two powerful modes.

Works on **Arch Linux, Manjaro, Fedora, Ubuntu, Debian, …** (tested 2025).

## Prerequisites

- Python 3.10+
- `pipx` (strongly recommended)
- `ble.sh` (optional but highly recommended for key bindings)

## 1. Install in 2 minutes

```bash
# Clone the repository
git clone https://github.com/your-username/rapidstory.git ~/dev/rapidstory
cd ~/dev/rapidstory

# Install in editable mode (recommended)
pipx install --editable .

# Make user binaries available (once only)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

If `pipx` is not yet installed:

```bash
# Arch / Manjaro
sudo pacman -S python-pipx

# Ubuntu / Debian
sudo apt install pipx

# Fedora
sudo dnf install pipx
```

## 2. Shell integration (ble.sh – recommended)

Add these functions to the end of your `~/.bashrc`:

```bash
# RapidStory – Ctrl+R (full-screen) & Ctrl+Up (inline)
__rapidstory_search() {
  local output result
  history -a
  output=$(rapidstory 2>/dev/null) || return
  result="${output%%|EXECUTE|*}"
  result="${result%"${result##*[![:space:]]}"}"

  [[ -z "$result" ]] && return
  [[ "$result" =~ rm[[:space:]]+-rf[[:space:]]+/ ]] && return

  if [[ "$output" == *"|EXECUTE|"* ]]; then
    history -s "$result"
    printf '%s%s\n' "${PS1@P}" "$result"
    eval "$result"
    READLINE_LINE=""; READLINE_POINT=0
  else
    READLINE_LINE="$result"; READLINE_POINT=${#result}
  fi
}

__rapidstory_inline_search() {
  local output result
  history -a
  output=$(rapidstory --inline 2>/dev/null) || return
  result="${output%%|EXECUTE|*}"
  result="${result%"${result##*[![:space:]]}"}"

  [[ -z "$result" ]] && return
  [[ "$result" =~ rm[[:space:]]+-rf[[:space:]]+/ ]] && return

  if [[ "$output" == *"|EXECUTE|"* ]]; then
    history -s "$result"
    printf '%s%s\n' "${PS1@P}" "$result"
    eval "$result"
    READLINE_LINE=""; READLINE_POINT=0
  else
    READLINE_LINE="$result"; READLINE_POINT=${#result}
  fi
}

export -f __rapidstory_search __rapidstory_inline_search
```

Add the key bindings to `~/.blerc` (or your ble.sh bindings file):

```bash
ble-bind -x 'C-r' '__rapidstory_search'
ble-bind -x 'C-up' '__rapidstory_inline_search'
```

Reload:

```bash
source ~/.bashrc
```

Ctrl+R and Ctrl+Up are now ready!

## 3. Updating / Reinstalling after code changes

A tiny helper script is shipped with the project:

```bash
# From anywhere (you can add this alias to ~/.bashrc)
rs() { ~/dev/rapidstory/scripts/install.sh; }

# Or run it directly
cd ~/dev/rapidstory && ./scripts/install.sh
```

**`scripts/install.sh`** – Official reinstall script (always up-to-date)

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="${BASH_SOURCE[0]}"
PROJECT_DIR="$(cd "$(dirname "$SCRIPT_PATH")/.." && pwd)"
BIN_NAME="rapidstory"

echo "RapidStory – Smart installer / updater"
echo "============================================"

# Ensure ~/.local/bin is in PATH
if ! grep -q '\.local/bin' "$HOME/.bashrc" 2>/dev/null; then
  echo "Adding ~/.local/bin to PATH in ~/.bashrc"
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
  export PATH="$HOME/.local/bin:$PATH"
fi

echo "Installing/updating RapidStory with pipx (editable mode)..."
if pipx list --short | grep -q "^$BIN_NAME "; then
  echo "RapidStory already installed → reinstalling..."
  printf 'y\n' | pipx uninstall "$BIN_NAME"
  pipx install --editable "$PROJECT_DIR"
else
  echo "First installation..."
  pipx install --editable "$PROJECT_DIR"
fi

if command -v "$BIN_NAME" >/dev/null; then
  echo ""
  echo "SUCCESS! RapidStory is up-to-date."
  echo "Ctrl+R and Ctrl+Up are ready."
else
  echo "ERROR: $BIN_NAME not found"
  exit 1
fi
echo "All done!"
```

Just run `./scripts/install.sh` (or the `rs` alias) after every code change – everything is rebuilt instantly.

## Uninstalling

```bash
pipx uninstall rapidstory
```

## User configuration

```
~/.local/share/rapidstory/config.py
```

Fully documented → see [`docs/CONFIGURATION.md`](docs/CONFIGURATION.md)

Enjoy the fastest Bash history experience you’ve ever had!

— Clément Stoyanov © 2025
```
