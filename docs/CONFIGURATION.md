```markdown
# RapidStory Configuration

All settings are stored in a single, easy-to-edit Python file:

```
~/.local/share/rapidstory/config.py
```

The file is automatically created the first time you run RapidStory.  
You can edit it anytime — changes take effect immediately.

---

### File location
```bash
~/.local/share/rapidstory/config.py
```

---

### Full example (default values + comments)

```python
# ============================================================================
# GLOBAL SETTINGS
# ============================================================================

# Maximum number of commands loaded into memory from ~/.bash_history
HISTORY_LOAD_LIMIT = 3000

# Bash history size (HISTSIZE / HISTFILESIZE)
HISTSIZE = 20000
HISTFILESIZE = 20000

# How often to append to history file (every N commands)
HISTORY_APPEND_FREQUENCY = 10

# How often (in seconds) to check ~/.bash_history for changes
MONITOR_INTERVAL = 30

# Minimum similarity score for fuzzy search (0.0 → 1.0)
FUZZY_SEARCH_THRESHOLD = 0.5

# Delimiter to force literal search on numbers
# Example: '8000' → searches for "8000" instead of selecting line 8000
SEARCH_MODE_DELIMITER = "'"

# ============================================================================
# FULL-SCREEN MODE (Ctrl+R)
# ============================================================================

DISPLAY_LIMIT = 20                     # Number of results shown
MAX_COMMAND_DISPLAY_LENGTH = 80       # Truncate long commands
EXECUTE_DIRECTLY_FULL_MODE = True     # Pressing Enter executes the command

# Navigation direction (True = Up = older, Down = newer → like native Bash)
FULL_REVERSE_NAVIGATION = False

FULL_ACTIVE_INDICATOR = "→"
FULL_ACTIVE_LINE_FG = "white"
FULL_ACTIVE_LINE_BG = "blue"
FULL_ACTIVE_LINE_ATTR = "bold"

FULL_NORMAL_LINE_FG = "white"
FULL_NORMAL_LINE_BG = None
FULL_NORMAL_LINE_ATTR = None

FULL_NUMBER_FG = "yellow"
FULL_NUMBER_BG = None
FULL_NUMBER_ATTR = "bold"

# ============================================================================
# INLINE MODE (Ctrl+Up)
# ============================================================================

INLINE_SUGGESTIONS_LIMIT = 3           # Number of suggestions below the prompt
EXECUTE_DIRECTLY_INLINE_MODE = True    # Enter executes directly

# Navigation direction in inline mode
INLINE_REVERSE_NAVIGATION = True       # True = Up = older

INLINE_CURRENT_INDICATOR = "→"
INLINE_CURRENT_FG = "white"
INLINE_CURRENT_BG = "blue"
INLINE_CURRENT_ATTR = "bold"

INLINE_SUGGESTION_FG = "white"
INLINE_SUGGESTION_BG = None
INLINE_SUGGESTION_ATTR = None

INLINE_NUMBER_FG = "yellow"
INLINE_NUMBER_BG = None
INLINE_NUMBER_ATTR = "bold"

# ============================================================================
# ANSI COLOR CODES (usable everywhere)
# ============================================================================

# Named colors: "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"
# 256 colors: "242", "237", "15", etc.
# RGB hex: "#5FAFFF", "#FF5F87", "#87D700"
# RGB decimal: "95,175,255"
# Attributes: "bold", "dim", "underline", "reverse", None

# Nice theme examples:
# INLINE_CURRENT_BG = "237"           # elegant dark gray
# FULL_ACTIVE_LINE_FG = "#5FAFFF"     # light blue
# FULL_ACTIVE_LINE_ATTR = "bold"
```

---

### Customization tips

```python
# Dark elegant theme
FULL_ACTIVE_LINE_BG = "236"
FULL_NORMAL_LINE_FG = "252"
INLINE_CURRENT_BG = "236"
INLINE_CURRENT_FG = "#87FFAF"   # mint green

# Solarized-like theme
FULL_ACTIVE_LINE_BG = "blue"
FULL_ACTIVE_LINE_FG = "white"
FULL_ACTIVE_LINE_ATTR = "bold"
```

---

### Reload configuration

No restart needed!  
Just press `Ctrl+R` or `Ctrl+Up` again — the new config is loaded instantly.

---
```
