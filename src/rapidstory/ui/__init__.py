# Expose les classes et modules principaux pour imports simples
# (from ui import FullModeUI, etc.)

from .ui_full_mode import FullModeUI, FullModeDisplay
from .ui_inline_mode import InlineModeUI, InlineModeDisplay
from .colors import ColorFormatter
from .ui_global import (
    KeyboardInput,
    is_quit_key,
    is_navigation_up,
    is_navigation_down,
    is_enter,
    is_backspace,
    is_digit_selection,
    KEY_ESC,
    KEY_CTRL_C,
    KEY_CTRL_D,
    KEY_CTRL_R,
    KEY_ENTER,
    KEY_ENTER_ALT,
    KEY_BACKSPACE,
    SEQ_ARROW_UP,
    SEQ_ARROW_DOWN,
    SEQ_CTRL_UP,
)

__all__ = [
    "FullModeUI",
    "FullModeDisplay",
    "InlineModeUI",
    "InlineModeDisplay",
    "ColorFormatter",
    "KeyboardInput",
    "is_quit_key",
    "is_navigation_up",
    "is_navigation_down",
    "is_enter",
    "is_backspace",
    "is_digit_selection",
    "KEY_ESC",
    "KEY_CTRL_C",
    "KEY_CTRL_D",
    "KEY_CTRL_R",
    "KEY_ENTER",
    "KEY_ENTER_ALT",
    "KEY_BACKSPACE",
    "SEQ_ARROW_UP",
    "SEQ_ARROW_DOWN",
    "SEQ_CTRL_UP",
]
