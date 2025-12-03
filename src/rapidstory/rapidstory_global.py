import sys
from typing import Optional, Tuple, Dict, List
from abc import ABC, abstractmethod

from .utils import ConfigLoader, CommandValidator
from .database import HistoryManager
from .search import SearchEngine, QueryParser
from .ui.ui_protocol import UIProtocol
from .ui.ui_global import (
    is_quit_key,
    is_enter,
    is_backspace,
    is_digit_selection,
    is_navigation_up,
    is_navigation_down,
    KEY_ESC,
)


class RapidStoryGlobal(ABC):
    """
    Classe abstraite pour les modes RapidStory.

    Responsabilité : Définir le comportement commun (recherche, navigation, sorties).
    Les enfants déclarent UNIQUEMENT leur touche de toggle et leurs spécificités UI.

    Principe Template Method : run() orchestre, les sous-classes implémentent les détails.
    """

    # Attribut à définir obligatoirement dans les classes filles
    TOGGLE_KEY: str

    def __init__(self):
        """Initialise les composants communs et valide TOGGLE_KEY."""
        # Vérifie que l'enfant a défini TOGGLE_KEY
        if not hasattr(self, "TOGGLE_KEY"):
            raise NotImplementedError(
                f"{self.__class__.__name__} doit définir TOGGLE_KEY"
            )

        self.config = ConfigLoader()

        self.history = HistoryManager(
            db_path=self.config.get("DB_PATH"),
            history_path=self.config.get("BASH_HISTORY_PATH"),
            load_limit=self.config.get("HISTORY_LOAD_LIMIT"),
            monitor_interval=self.config.get("MONITOR_INTERVAL"),
        )

        query_parser = QueryParser(delimiter=self.config.get("SEARCH_MODE_DELIMITER"))
        self.search = SearchEngine(
            threshold=self.config.get("FUZZY_SEARCH_THRESHOLD"),
            query_parser=query_parser,
        )

        self.validator = CommandValidator()
        self.ui: UIProtocol = self._create_ui()

        self.history.load_from_file()

    @abstractmethod
    def _create_ui(self) -> UIProtocol:
        """Crée l'UI spécifique au mode (Full ou Inline)."""
        pass

    @abstractmethod
    def _get_initial_state(self) -> Dict:
        """Retourne l'état initial (query, index, results)."""
        pass

    @abstractmethod
    def _render(self, state: Dict) -> None:
        """Affiche l'UI avec l'état actuel."""
        pass

    @abstractmethod
    def _handle_digit_selection(
        self, key: str, state: Dict
    ) -> Optional[Tuple[str, bool]]:
        """Gère la sélection par chiffre (logique différente Full/Inline)."""
        pass

    @abstractmethod
    def _move_up(self, state: Dict) -> Dict:
        """Navigation haut (respecte REVERSE_NAVIGATION)."""
        pass

    @abstractmethod
    def _move_down(self, state: Dict) -> Dict:
        """Navigation bas (respecte REVERSE_NAVIGATION)."""
        pass

    @abstractmethod
    def _select_current(self, state: Dict) -> Optional[Tuple[str, bool]]:
        """Sélectionne la commande actuelle."""
        pass

    @abstractmethod
    def _get_search_limit(self) -> int:
        """Retourne la limite de recherche (Full vs Inline)."""
        pass

    @abstractmethod
    def _create_search_update(self, query: str, results: List[str]) -> Dict:
        """Crée l'état mis à jour après recherche (reset index)."""
        pass

    def run(self) -> Optional[Tuple[str, bool]]:
        """
        Lance la boucle interactive (Template Method).

        Returns:
            (commande, execute_directly) ou None si annulation
        """
        state = self._get_initial_state()

        self.ui.setup()

        try:
            return self._interaction_loop(state)

        except (KeyboardInterrupt, EOFError):
            return None

        except (IOError, OSError) as e:
            sys.stderr.write(f"Erreur TTY : {e}\n")
            return None

        finally:
            self.ui.cleanup()

    def _interaction_loop(self, state: Dict) -> Optional[Tuple[str, bool]]:
        """Boucle principale d'interaction."""
        while True:
            self._render(state)

            key = self.ui.wait_for_input()

            action = self._handle_key(key, state)

            if action is None:
                continue
            elif action == "QUIT":
                return None
            elif isinstance(action, dict):
                state.update(action)
            elif isinstance(action, tuple):
                return action

    def _handle_key(self, key: str, state: Dict):
        """
        Gère une touche (logique commune).

        Sorties définies centralement :
        - Ctrl+C, Ctrl+D : is_quit_key()
        - ESC seul : séquence None
        - Toggle : TOGGLE_KEY (Ctrl+R pour Full, Ctrl+Up pour Inline)
        """
        # Sortie standard : Ctrl+C, Ctrl+D
        if is_quit_key(key):
            return "QUIT"

        # Toggle : caractère direct (Ctrl+R = \x12)
        if key == self.TOGGLE_KEY:
            return "QUIT"

        # ESC : séquence ou sortie
        if key == KEY_ESC:
            seq = self.ui.handle_escape()

            # ESC seul = quitter
            if seq is None:
                return "QUIT"

            # Toggle : séquence ESC (Ctrl+Up = [1;5A)
            if seq == self.TOGGLE_KEY:
                return "QUIT"

            # Navigation
            if is_navigation_up(seq):
                return self._move_up(state)
            elif is_navigation_down(seq):
                return self._move_down(state)

        if is_enter(key):
            return self._select_current(state)

        if is_backspace(key):
            return self._handle_backspace(state)

        # Mode recherche : tout va dans la query
        if self.search.is_in_search_mode(state["query"]):
            return self._handle_char(key, state)

        # Hors mode recherche : chiffres = sélection
        if is_digit_selection(key):
            return self._handle_digit_selection(key, state)

        # Tout le reste = recherche
        return self._handle_char(key, state)

    def _handle_backspace(self, state: Dict) -> Dict:
        """Supprime le dernier caractère de la recherche."""
        query = state["query"][:-1]
        results = self._search(query)
        return self._create_search_update(query, results)

    def _handle_char(self, char: str, state: Dict) -> Dict:
        """Ajoute un caractère à la recherche."""
        query = state["query"] + char
        results = self._search(query)
        return self._create_search_update(query, results)

    def _search(self, query: str) -> List[str]:
        """Effectue une recherche dans l'historique."""
        commands = self.history.get_commands()
        limit = self._get_search_limit()
        return self.search.search(query, commands, limit)
