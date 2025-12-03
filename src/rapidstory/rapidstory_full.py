from typing import Optional, Tuple, Dict, List

from .rapidstory_global import RapidStoryGlobal
from .ui import FullModeUI
from .ui.ui_protocol import UIProtocol
from .ui.ui_global import KEY_CTRL_R


class RapidStoryFull(RapidStoryGlobal):
    """Mode full-screen (Ctrl+R)."""

    # Déclaration raccourci ouverture pour toggle fermeture
    TOGGLE_KEY = KEY_CTRL_R  # Seule déclaration spécifique

    def _create_ui(self) -> UIProtocol:
        """Crée l'UI full-screen."""
        return FullModeUI(
            max_command_length=self.config.get("MAX_COMMAND_DISPLAY_LENGTH"),
            config=self.config.get_all(),
        )

    def _get_initial_state(self) -> Dict:
        """État initial : query vide, index 1, recherche complète."""
        return {
            "query": "",
            "active_index": 1,
            "results": self._search(""),
        }

    def _render(self, state: Dict) -> None:
        """Affiche l'UI full-screen."""
        self.ui.render(state["query"], state["results"], state["active_index"])

    def _get_search_limit(self) -> int:
        """Limite d'affichage mode full."""
        return self.config.get("DISPLAY_LIMIT")

    def _create_search_update(self, query: str, results: List[str]) -> Dict:
        """Reset index à 1 après recherche."""
        return {"query": query, "results": results, "active_index": 1}

    def _move_up(self, state: Dict) -> Dict:
        """Navigation haut (respecte FULL_REVERSE_NAVIGATION)."""
        results = state["results"]
        active_index = state["active_index"]

        if not results:
            return {"active_index": active_index}

        reverse_nav = self.config.get("FULL_REVERSE_NAVIGATION")

        if reverse_nav:
            if active_index < len(results):
                active_index += 1
        else:
            if active_index > 1:
                active_index -= 1

        return {"active_index": active_index}

    def _move_down(self, state: Dict) -> Dict:
        """Navigation bas (respecte FULL_REVERSE_NAVIGATION)."""
        results = state["results"]
        active_index = state["active_index"]

        if not results:
            return {"active_index": active_index}

        reverse_nav = self.config.get("FULL_REVERSE_NAVIGATION")

        if reverse_nav:
            if active_index > 1:
                active_index -= 1
        else:
            if active_index < len(results):
                active_index += 1

        return {"active_index": active_index}

    def _select_current(self, state: Dict) -> Optional[Tuple[str, bool]]:
        """Sélectionne la commande active avec Entrée."""
        results = state["results"]
        active_index = state["active_index"]

        if results and 0 < active_index <= len(results):
            command = results[active_index - 1]
            if self.validator.is_valid(command):
                return (command, self.config.get("EXECUTE_DIRECTLY_FULL_MODE"))

        return None

    def _handle_digit_selection(
        self, key: str, state: Dict
    ) -> Optional[Tuple[str, bool]]:
        """Sélection par position relative (1-9)."""
        num = int(key)
        active_index = state["active_index"]
        results = state["results"]

        target_index = active_index + (num - 1)

        if 1 <= target_index <= len(results):
            command = results[target_index - 1]
            if self.validator.is_valid(command):
                return (command, False)

        return None

    def _allows_toggle_shortcut(self) -> bool:
        """Mode full : Ctrl+R ferme l'interface."""
        return True
