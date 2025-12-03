import os
import re
from typing import Dict, Any


class ConfigLoader:
    """
    Charge et gère la configuration de l'application.

    Lit config.py et fusionne avec les valeurs par défaut.
    Responsabilité unique : gestion centralisée de la configuration.
    """

    def __init__(self, config_path: str = "~/.local/share/rapidstory/config.py"):
        self.config_path = os.path.expanduser(config_path)
        self.defaults = {
            "DISPLAY_LIMIT": 20,
            "HISTORY_LOAD_LIMIT": 1000,
            "HISTSIZE": 10000,
            "HISTFILESIZE": 20000,
            "MONITOR_INTERVAL": 30,
            "HISTORY_APPEND_FREQUENCY": 10,
            "DB_PATH": "~/.local/share/rapidstory/rapidstory.db",
            "BASH_HISTORY_PATH": "~/.bash_history",
            "FUZZY_SEARCH_THRESHOLD": 0.5,
            "SEARCH_MODE_DELIMITER": "'",
            "EXECUTE_DIRECTLY_FULL_MODE": True,
            "MAX_COMMAND_DISPLAY_LENGTH": 80,
            "FULL_EXTEND_BACKGROUND": True,
            "FULL_REVERSE_NAVIGATION": True,
            "FULL_SUGGESTIONS_POSITION": "bottom",
            "FULL_ACTIVE_INDICATOR": "→",
            "FULL_ACTIVE_INDICATOR_FG": None,
            "FULL_ACTIVE_INDICATOR_BG": None,
            "FULL_ACTIVE_INDICATOR_ATTR": None,
            "FULL_ACTIVE_LINE_FG": None,
            "FULL_ACTIVE_LINE_BG": None,
            "FULL_ACTIVE_LINE_ATTR": None,
            "FULL_NORMAL_LINE_FG": None,
            "FULL_NORMAL_LINE_BG": None,
            "FULL_NORMAL_LINE_ATTR": None,
            "FULL_NUMBER_FG": None,
            "FULL_NUMBER_BG": None,
            "FULL_NUMBER_ATTR": None,
            "EXECUTE_DIRECTLY_INLINE_MODE": True,
            "INLINE_SUGGESTIONS_LIMIT": 3,
            "INLINE_REVERSE_NAVIGATION": True,
            "INLINE_SUGGESTIONS_POSITION": "bottom",
            "INLINE_CURRENT_INDICATOR": "→",
            "INLINE_CURRENT_INDICATOR_FG": None,
            "INLINE_CURRENT_INDICATOR_BG": None,
            "INLINE_CURRENT_INDICATOR_ATTR": None,
            "INLINE_CURRENT_FG": None,
            "INLINE_CURRENT_BG": None,
            "INLINE_CURRENT_ATTR": None,
            "INLINE_SUGGESTION_FG": None,
            "INLINE_SUGGESTION_BG": None,
            "INLINE_SUGGESTION_ATTR": None,
            "INLINE_NUMBER_FG": None,
            "INLINE_NUMBER_BG": None,
            "INLINE_NUMBER_ATTR": None,
            "INLINE_SEARCH_LABEL_FG": None,
            "INLINE_SEARCH_LABEL_BG": None,
            "INLINE_SEARCH_LABEL_ATTR": None,
        }
        self.config = self.defaults.copy()
        self._load()

    def _load(self) -> None:
        """Charge la configuration depuis le fichier Python."""
        if not os.path.exists(self.config_path):
            return

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                code = compile(f.read(), self.config_path, "exec")
                namespace = {}
                exec(code, namespace)

                for key in self.defaults:
                    if key in namespace:
                        self.config[key] = namespace[key]

        except Exception:
            pass

    def get(self, key: str) -> Any:
        """Récupère une valeur de configuration."""
        return self.config.get(key, self.defaults.get(key))

    def get_all(self) -> Dict[str, Any]:
        """Retourne toute la configuration."""
        return self.config.copy()


class CommandValidator:
    """
    Valide et filtre les commandes.

    Responsabilité unique : vérification de sécurité des commandes.
    Principe Open/Closed : ajoute patterns sans modifier is_valid().
    """

    DANGEROUS_PATTERNS = [
        r"rm\s+-rf\s+/",
        r":\(\)\{.*\}",
    ]

    @staticmethod
    def is_valid(command: str) -> bool:
        """
        Vérifie si une commande est valide et sûre.

        Args:
            command: Commande à valider

        Returns:
            True si valide, False sinon
        """
        if not command or not command.strip():
            return False

        for pattern in CommandValidator.DANGEROUS_PATTERNS:
            if re.search(pattern, command):
                return False

        return True

    @staticmethod
    def sanitize(command: str) -> str:
        """
        Nettoie une commande (supprime espaces superflus).

        Args:
            command: Commande à nettoyer

        Returns:
            Commande nettoyée
        """
        return command.strip()
