```markdown
# RapidStory

**Ultra-fast Bash history search with a modern interface**

A lightning-fast, beautiful replacement for the classic `Ctrl+R` and ↑ key.

Two powerful modes:
- **Full-screen mode** (`Ctrl+R`) – rich TUI with numbered results, arrow navigation and digit selection
- **Inline mode** (`Ctrl+Up`) – compact suggestions directly under the prompt

Inspired by Atuin, built from scratch to be **fast, minimal and perfectly tailored**.

## Features

- Blazing-fast fuzzy + exact search (powered by `rapidfuzz`)
- Literal number search: `'8000'` → searches for “8000” instead of selecting line 8000
- Real-time monitoring of `~/.bash_history`
- Safety: blocks dangerous patterns (`rm -rf /`, etc.)
- Full duplicate removal (keeps only the latest occurrence)
- 100 % configurable colors, limits and behavior
- Zero external dependencies except `rapidfuzz`

## Installation (less than 2 minutes)

```bash
git clone https://github.com/your-username/rapidstory.git ~/dev/rapidstory
cd ~/dev/rapidstory
pipx install --editable .
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

See the complete guide → [`docs/INSTALLATION.md`](docs/INSTALLATION.md)

## Shell integration (ble.sh recommended)

Add the provided functions to your `~/.bashrc` and bind them in `~/.blerc`:

```bash
# ~/.blerc
ble-bind -x 'C-r' '__rapidstory_search'
ble-bind -x 'C-up' '__rapidstory_inline_search'
```

Full instructions → [`docs/INSTALLATION.md`](docs/INSTALLATION.md)

## Update / Reinstall after code changes

A smart script is included to keep everything in sync:

```bash
# From anywhere (add this alias to ~/.bashrc)
alias rs='~/dev/rapidstory/scripts/install.sh'

# Or run directly
~/dev/rapidstory/scripts/install.sh
```

Just run `rs` after any code change — RapidStory is rebuilt instantly.

**`scripts/install.sh`** – Official update script

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="${BASH_SOURCE[0]}"
PROJECT_DIR="$(cd "$(dirname "$SCRIPT_PATH")/.." && pwd)"
BIN_NAME="rapidstory"

echo "RapidStory – Smart installer / updater"
echo "============================================"

# Ensure PATH
if ! grep -q '\.local/bin' "$HOME/.bashrc" 2>/dev/null; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
  export PATH="$HOME/.local/bin:$PATH"
fi

echo "Installing/updating RapidStory..."
if pipx list --short | grep -q "^$BIN_NAME "; then
  printf 'y\n' | pipx uninstall "$BIN_NAME"
fi
pipx install --editable "$PROJECT_DIR"

echo ""
echo "SUCCESS! RapidStory is up-to-date."
echo "Ctrl+R and Ctrl+Up are ready."
```

## Configuration

All settings are in:

```
~/.local/share/rapidstory/config.py
```

Fully documented with examples → [`docs/CONFIGURATION.md`](docs/CONFIGURATION.md)

## Updating

```bash
cd ~/dev/rapidstory
git pull
rs   # or ./scripts/install.sh
```

## Uninstalling

```bash
pipx uninstall rapidstory
```

## License

MIT © Clément Stoyanov – 2025

---

**Enjoy the fastest, most beautiful Bash history experience you've ever had.**

Star the repo if you like it — contributions welcome!
