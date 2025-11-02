import sys
import tty
import termios
import os
import fcntl
from typing import Optional


KEY_CTRL_C = "\x03"
KEY_CTRL_D = "\x04"
KEY_CTRL_R = "\x12"
KEY_ESC = "\x1b"
KEY_ENTER = "\n"
KEY_ENTER_ALT = "\r"
KEY_BACKSPACE = "\x7f"
SEQ_ARROW_UP = "[A"
SEQ_ARROW_DOWN = "[B"
SEQ_CTRL_UP = "[1;5A"


class KeyboardInput:
    """
    Gère la lecture brute des entrées clavier en mode cbreak.

    Responsabilité unique : capture des touches sans interprétation.
    """

    def __init__(self):
        self.fd = sys.stdin.fileno()
        self.old_settings = None

    def setup(self) -> None:
        """Active le mode cbreak (lecture caractère par caractère)."""
        self.old_settings = termios.tcgetattr(self.fd)
        tty.setcbreak(self.fd)

    def cleanup(self) -> None:
        """Restaure les paramètres originaux du terminal."""
        if self.old_settings:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)

    def read_key(self) -> str:
        """
        Lit un seul caractère depuis stdin.

        Returns:
            Caractère lu (ex: 'a', '\n', '\x1b')
        """
        return sys.stdin.read(1)

    def read_escape_sequence(self) -> Optional[str]:
        """
        Lit une séquence d'échappement ANSI.

        Returns:
            Séquence lue (ex: '[A', '[1;5A') ou None
        """
        try:
            flags = fcntl.fcntl(self.fd, fcntl.F_GETFL)
            fcntl.fcntl(self.fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

            try:
                # Lit jusqu'à 6 caractères pour Ctrl+Up/Down
                seq = sys.stdin.read(6)
                return seq.rstrip("\x00") if seq else None
            finally:
                fcntl.fcntl(self.fd, fcntl.F_SETFL, flags)

        except (IOError, OSError):
            return None


def is_quit_key(key: str) -> bool:
    """Vérifie si c'est une touche de sortie (Ctrl+C ou Ctrl+D)."""
    return key in (KEY_CTRL_C, KEY_CTRL_D)


def is_navigation_up(seq: str) -> bool:
    """Vérifie si c'est la flèche haut."""
    return seq == SEQ_ARROW_UP


def is_navigation_down(seq: str) -> bool:
    """Vérifie si c'est la flèche bas."""
    return seq == SEQ_ARROW_DOWN


def is_enter(key: str) -> bool:
    """Vérifie si c'est la touche Entrée."""
    return key in (KEY_ENTER, KEY_ENTER_ALT)


def is_backspace(key: str) -> bool:
    """Vérifie si c'est Backspace."""
    return key == KEY_BACKSPACE


def is_digit_selection(key: str) -> bool:
    """Vérifie si c'est un chiffre 1-9 (sélection de commande)."""
    return key.isdigit() and key != "0"
