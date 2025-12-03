from typing import Optional, Tuple, Dict, List

from .rapidstory_global import RapidStoryGlobal
from .ui.ui_inline_mode import InlineModeUI
from .ui.ui_protocol import UIProtocol
from .ui.ui_global import SEQ_CTRL_UP


class RapidStoryInline(RapidStoryGlobal):
    """Mode inline (Ctrl+Up)."""

    # Déclaration raccourci ouverture
    TOGGLE_KEY = SEQ_CTRL_UP  # Seule déclaration spécifique

    def _create_ui(self) -> UIProtocol:
        """Crée l'UI inline."""
        return InlineModeUI(
            suggestions_limit=self.config.get("INLINE_SUGGESTIONS_LIMIT"),
            config=self.config.get_all(),
        )

    def _get_initial_state(self) -> Dict:
        """État initial : query vide, index 0, recherche complète."""
        return {
            "query": "",
            "current_index": 0,
            "all_results": self._search(""),
        }

    def _render(self, state: Dict) -> None:
        """Affiche l'UI inline avec commande actuelle + suggestions."""
        all_results = state["all_results"]
        current_index = state["current_index"]

        current_cmd = all_results[current_index] if all_results else ""
        suggestions = self._get_suggestions(all_results, current_index)

        self.ui.render(state["query"], current_cmd, suggestions)

    def _get_search_limit(self) -> int:
        """Limite plus large pour suggestions inline."""
        return self.config.get("INLINE_SUGGESTIONS_LIMIT") + 50

    def _create_search_update(self, query: str, results: List[str]) -> Dict:
        """Reset index à 0 après recherche."""
        return {"query": query, "all_results": results, "current_index": 0}

    def _move_up(self, state: Dict) -> Dict:
        """Navigation haut (respecte INLINE_REVERSE_NAVIGATION)."""
        all_results = state["all_results"]
        current_index = state["current_index"]

        if not all_results:
            return {"current_index": current_index}

        reverse_nav = self.config.get("INLINE_REVERSE_NAVIGATION")

        if reverse_nav:
            if current_index < len(all_results) - 1:
                current_index += 1
        else:
            if current_index > 0:
                current_index -= 1

        return {"current_index": current_index}

    def _move_down(self, state: Dict) -> Dict:
        """Navigation bas (respecte INLINE_REVERSE_NAVIGATION)."""
        all_results = state["all_results"]
        current_index = state["current_index"]

        if not all_results:
            return {"current_index": current_index}

        reverse_nav = self.config.get("INLINE_REVERSE_NAVIGATION")

        if reverse_nav:
            if current_index > 0:
                current_index -= 1
        else:
            if current_index < len(all_results) - 1:
                current_index += 1

        return {"current_index": current_index}

    def _select_current(self, state: Dict) -> Optional[Tuple[str, bool]]:
        """Sélectionne la commande actuelle avec Entrée."""
        all_results = state["all_results"]
        current_index = state["current_index"]

        if all_results and 0 <= current_index < len(all_results):
            command = all_results[current_index]
            if self.validator.is_valid(command):
                return (command, self.config.get("EXECUTE_DIRECTLY_INLINE_MODE"))

        return None

    def _handle_digit_selection(
        self, key: str, state: Dict
    ) -> Optional[Tuple[str, bool]]:
        """Sélection inline : 1=current, 2-4=suggestions."""
        num = int(key)
        all_results = state["all_results"]
        current_index = state["current_index"]

        current_cmd = all_results[current_index] if all_results else ""
        suggestions = self._get_suggestions(all_results, current_index)

        if num == 1:
            if current_cmd and self.validator.is_valid(current_cmd):
                return (current_cmd, False)
            return None

        suggestion_index = num - 2
        if 0 <= suggestion_index < len(suggestions):
            command = suggestions[suggestion_index]
            if self.validator.is_valid(command):
                return (command, self.config.get("EXECUTE_DIRECTLY_INLINE_MODE"))

        return None

    def _get_suggestions(self, all_results: List[str], current_index: int) -> List[str]:
        """Récupère les suggestions après la commande actuelle."""
        suggestions_limit = self.config.get("INLINE_SUGGESTIONS_LIMIT")
        start = current_index + 1
        end = start + suggestions_limit
        return all_results[start:end]
