import sys
import shutil
from typing import List, Dict, Any, Optional

from .colors import ColorFormatter
from .ui_global import KeyboardInput


class InlineModeDisplay:
    """
    Affichage pur du mode inline (compact).

    Responsabilité unique : génération de l'affichage inline avec position configurable.
    Aucune logique métier, uniquement du formatage visuel.
    """

    def __init__(self, suggestions_limit: int, config: Dict[str, Any]):
        self.suggestions_limit = min(suggestions_limit, 9)
        self.config = config
        self.tty_out = None

        self.terminal_width = self._get_terminal_width()
        self._prepare_colors()

    def _get_terminal_width(self) -> int:
        """Récupère la largeur du terminal pour tronquer cmds."""
        try:
            return shutil.get_terminal_size().columns
        except Exception:
            return 80

    def _prepare_colors(self) -> None:
        """Prépare les codes ANSI depuis la configuration."""
        self.current_color = ColorFormatter.format(
            self.config.get("INLINE_CURRENT_FG"),
            self.config.get("INLINE_CURRENT_BG"),
            self.config.get("INLINE_CURRENT_ATTR"),
        )

        self.indicator_color = ColorFormatter.format(
            self.config.get("INLINE_CURRENT_INDICATOR_FG"),
            self.config.get("INLINE_CURRENT_INDICATOR_BG"),
            self.config.get("INLINE_CURRENT_INDICATOR_ATTR"),
        )

        self.indicator = self.config.get("INLINE_CURRENT_INDICATOR") or "→"

        self.suggestion_color = ColorFormatter.format(
            self.config.get("INLINE_SUGGESTION_FG"),
            self.config.get("INLINE_SUGGESTION_BG"),
            self.config.get("INLINE_SUGGESTION_ATTR"),
        )

        self.number_color = ColorFormatter.format(
            self.config.get("INLINE_NUMBER_FG"),
            self.config.get("INLINE_NUMBER_BG"),
            self.config.get("INLINE_NUMBER_ATTR"),
        )

        self.search_label_color = ColorFormatter.format(
            self.config.get("INLINE_SEARCH_LABEL_FG"),
            self.config.get("INLINE_SEARCH_LABEL_BG"),
            self.config.get("INLINE_SEARCH_LABEL_ATTR"),
        )

        self.reset = ColorFormatter.reset()

    def setup(self) -> None:
        """Ouvre le terminal pour écriture directe."""
        try:
            self.tty_out = open("/dev/tty", "w")
        except IOError:
            self.tty_out = None

    def cleanup(self) -> None:
        """Efface l'affichage et ferme le terminal."""
        if self.tty_out:
            self.tty_out.write("\033[J")  # Clear jusqu'à la fin
            self.tty_out.flush()
            self.tty_out.close()
            self.tty_out = None
        else:
            sys.stdout.write("\033[J")
            sys.stdout.flush()

    def render(self, query: str, current: str, suggestions: List[str]) -> None:
        """
        Affiche la recherche inline.

        Args:
            query: Texte de recherche (affiché en haut)
            current: Commande courante (ligne 1)
            suggestions: Liste des suggestions suivantes
        """
        output = self._build_display(query, current, suggestions)

        try:
            if self.tty_out:
                self.tty_out.write(output)
                self.tty_out.flush()
            else:
                sys.stdout.write(output)
                sys.stdout.flush()
        except IOError:
            pass

    def _build_display(self, query: str, current: str, suggestions: List[str]) -> str:
        """
        Construit l'affichage inline complet.

        Gère deux positions : top (suggestions au-dessus) ou bottom (en-dessous).

        Returns:
            Chaîne ANSI formatée
        """
        output = []

        output.append("\033[s\033[2J")  # Save + full clear pour éviter wrapping

        if query:
            output.append(
                f"{self.search_label_color}[Recherche: {query}]{self.reset}\n"
            )

        indicator_width = len(self.indicator) + 1
        position = self.config.get("INLINE_SUGGESTIONS_POSITION", "bottom")
        max_cmd_len = max(
            0, self.terminal_width - 15
        )  # Padding pour num + indicator + "..."

        if position == "top":
            output.extend(
                self._build_top_layout(
                    current, suggestions, indicator_width, max_cmd_len
                )
            )
        else:
            output.extend(
                self._build_bottom_layout(
                    current, suggestions, indicator_width, max_cmd_len
                )
            )

        output.append("\033[u")  # Restaure position curseur

        return "".join(output)

    def _truncate_cmd(self, cmd: str, max_len: int) -> str:
        """Tronque une commande pour éviter wrapping."""
        if len(cmd) <= max_len:
            return cmd
        return f"{cmd[: max_len - 3]}..."

    def _build_top_layout(
        self,
        current: str,
        suggestions: List[str],
        indicator_width: int,
        max_cmd_len: int,
    ) -> List[str]:
        """
        Layout top : suggestions au-dessus de la commande actuelle.

        Ordre : ancien → récent (suggestions inversées)
        """
        lines = []

        reversed_suggestions = list(reversed(suggestions[: self.suggestions_limit]))
        total_suggestions = len(reversed_suggestions)

        for i, cmd in enumerate(reversed_suggestions):
            num = total_suggestions + 1 - i
            col_number = f"{self.number_color}{num}.{self.reset}"
            col_indicator = " " * indicator_width
            col_cmd = f"{self.suggestion_color}{self._truncate_cmd(cmd, max_cmd_len)}{self.reset}"
            lines.append(f"{col_number} {col_indicator}{col_cmd}\n")

        if current:
            col_number = f"{self.number_color}1.{self.reset}"
            col_indicator = f"{self.indicator_color}{self.indicator}{self.reset} "
            col_cmd = f"{self.current_color}{self._truncate_cmd(current, max_cmd_len)}{self.reset}"
            lines.append(f"{col_number} {col_indicator}{col_cmd}\n")

        return lines

    def _build_bottom_layout(
        self,
        current: str,
        suggestions: List[str],
        indicator_width: int,
        max_cmd_len: int,
    ) -> List[str]:
        """
        Layout bottom : commande actuelle puis suggestions en-dessous.

        Ordre naturel : récent → ancien
        """
        lines = []

        if current:
            col_number = f"{self.number_color}1.{self.reset}"
            col_indicator = f"{self.indicator_color}{self.indicator}{self.reset} "
            col_cmd = f"{self.current_color}{self._truncate_cmd(current, max_cmd_len)}{self.reset}"
            lines.append(f"{col_number} {col_indicator}{col_cmd}\n")

        for i, cmd in enumerate(suggestions[: self.suggestions_limit], 2):
            col_number = f"{self.number_color}{i}.{self.reset}"
            col_indicator = " " * indicator_width
            col_cmd = f"{self.suggestion_color}{self._truncate_cmd(cmd, max_cmd_len)}{self.reset}"
            lines.append(f"{col_number} {col_indicator}{col_cmd}\n")

        return lines


class InlineModeUI:
    """
    Interface utilisateur du mode inline.

    Orchestration : coordonne display + keyboard pour mode compact.
    """

    def __init__(self, suggestions_limit: int, config: Dict[str, Any]):
        self.display = InlineModeDisplay(suggestions_limit, config)
        self.keyboard = KeyboardInput()

    def setup(self) -> None:
        """Configure l'UI (keyboard + display)."""
        self.keyboard.setup()
        self.display.setup()

    def cleanup(self) -> None:
        """Restaure l'état original."""
        self.keyboard.cleanup()
        self.display.cleanup()

    def render(self, query: str, current: str, suggestions: List[str]) -> None:
        """Délègue l'affichage au display."""
        self.display.render(query, current, suggestions)

    def wait_for_input(self) -> str:
        """Attend une touche de l'utilisateur."""
        return self.keyboard.read_key()

    def handle_escape(self) -> Optional[str]:
        """
        Gère la touche Échap et lit la séquence.

        Returns:
            Séquence ANSI ou None
        """
        seq = self.keyboard.read_escape_sequence()
        if seq in ("[A", "[B", "[1;5A"):
            return seq
        return None
