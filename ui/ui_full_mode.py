import sys
from typing import List, Dict, Any, Optional

from .colors import ColorFormatter
from .ui_global import KeyboardInput


class FullModeDisplay:
    """
    Affichage pur du mode full-screen.

    Responsabilité unique : transformation données → texte ANSI formaté.
    Ne gère AUCUNE logique métier, seulement le rendu visuel.
    """

    def __init__(self, max_command_length: int, config: Dict[str, Any]):
        self.max_command_length = max_command_length
        self.config = config
        self.tty_out = None

        self.terminal_width = self._get_terminal_width()
        self._prepare_colors()

    def _get_terminal_width(self) -> int:
        """Récupère la largeur du terminal pour l'affichage."""
        try:
            import shutil

            return shutil.get_terminal_size().columns
        except Exception:
            return 80

    def _prepare_colors(self) -> None:
        """Prépare les codes ANSI à partir de la configuration."""
        self.active_line_color = ColorFormatter.format(
            self.config.get("FULL_ACTIVE_LINE_FG"),
            self.config.get("FULL_ACTIVE_LINE_BG"),
            self.config.get("FULL_ACTIVE_LINE_ATTR"),
        )

        self.normal_line_color = ColorFormatter.format(
            self.config.get("FULL_NORMAL_LINE_FG"),
            self.config.get("FULL_NORMAL_LINE_BG"),
            self.config.get("FULL_NORMAL_LINE_ATTR"),
        )

        self.number_color = ColorFormatter.format(
            self.config.get("FULL_NUMBER_FG"),
            self.config.get("FULL_NUMBER_BG"),
            self.config.get("FULL_NUMBER_ATTR"),
        )

        self.indicator_color = ColorFormatter.format(
            self.config.get("FULL_ACTIVE_INDICATOR_FG"),
            self.config.get("FULL_ACTIVE_INDICATOR_BG"),
            self.config.get("FULL_ACTIVE_INDICATOR_ATTR"),
        )

        self.indicator = self.config.get("FULL_ACTIVE_INDICATOR") or "→"
        self.reset = ColorFormatter.reset()

    def setup(self) -> None:
        """Active l'alternate screen et cache le curseur."""
        try:
            self.tty_out = open("/dev/tty", "w")
            self.tty_out.write("\033[?1049h")  # Alternate screen
            self.tty_out.write("\033[?25l")  # Cache curseur
            self.tty_out.flush()
        except IOError:
            self.tty_out = None

    def cleanup(self) -> None:
        """Restaure le terminal normal et affiche le curseur."""
        if self.tty_out:
            self.tty_out.write("\033[?1049l")  # Quitte alternate screen
            self.tty_out.write("\033[?25h")  # Affiche curseur
            self.tty_out.write("\n")
            self.tty_out.flush()
            self.tty_out.close()
            self.tty_out = None

    def render(self, query: str, results: List[str], active_index: int) -> None:
        """
        Affiche l'interface de recherche complète.

        Args:
            query: Texte de recherche actuel
            results: Liste des commandes trouvées
            active_index: Index de la ligne active (1-based)
        """
        output = self._build_display(query, results, active_index)

        try:
            if self.tty_out:
                self.tty_out.write(output)
                self.tty_out.flush()
            else:
                sys.stdout.write(output)
                sys.stdout.flush()
        except IOError:
            pass

    def _build_display(self, query: str, results: List[str], active_index: int) -> str:
        """
        Construit le contenu complet à afficher.

        Returns:
            Chaîne ANSI formatée prête à afficher
        """
        lines = []

        lines.append("\033[2J\033[H")  # Clear + home

        lines.append(f"Recherche : {query}")
        lines.append("-------------------")

        if not results:
            lines.append("Aucun résultat trouvé.")
        else:
            for i, cmd in enumerate(results):
                line = self._format_result_line(cmd, i + 1, active_index)
                lines.append(line)

        return "\n".join(lines)

    def _format_result_line(self, command: str, index: int, active_index: int) -> str:
        """
        Formate une ligne de résultat avec colonnes fixes.

        Structure : [numéro relatif] [indicateur] [commande]

        Args:
            command: Commande à afficher
            index: Position absolue (1-based)
            active_index: Position de la ligne active

        Returns:
            Ligne formatée avec codes ANSI
        """
        display_cmd = command[: self.max_command_length]
        if len(command) > self.max_command_length:
            display_cmd += "..."

        rel_pos = index - active_index + 1

        if 1 <= rel_pos <= 9:
            col_number = f"{self.number_color}{rel_pos}.{self.reset}"
        else:
            col_number = "  "

        indicator_width = len(self.indicator) + 1

        if index == active_index:
            col_indicator = f"{self.indicator_color}{self.indicator}{self.reset} "
        else:
            col_indicator = " " * indicator_width

        if index == active_index:
            col_command = f"{self.active_line_color}{display_cmd}{self.reset}"
        else:
            col_command = f"{self.normal_line_color}{display_cmd}{self.reset}"

        return f"{col_number} {col_indicator}{col_command}"


class FullModeUI:
    """
    Interface utilisateur du mode full-screen.

    Orchestration : coordonne display + keyboard.
    Principe de séparation : UI ≠ logique métier.
    """

    def __init__(self, max_command_length: int, config: Dict[str, Any]):
        self.display = FullModeDisplay(max_command_length, config)
        self.keyboard = KeyboardInput()

    def setup(self) -> None:
        """Configure l'UI (keyboard + display)."""
        self.keyboard.setup()
        self.display.setup()

    def cleanup(self) -> None:
        """Restaure l'état original du terminal."""
        self.keyboard.cleanup()
        self.display.cleanup()

    def render(self, query: str, results: List[str], active_index: int) -> None:
        """Délègue l'affichage au display."""
        self.display.render(query, results, active_index)

    def wait_for_input(self) -> str:
        """Attend une touche de l'utilisateur."""
        return self.keyboard.read_key()

    def handle_escape(self) -> Optional[str]:
        """
        Gère la touche Échap et lit la séquence complète.

        Returns:
            Séquence ANSI ou None
        """
        seq = self.keyboard.read_escape_sequence()
        if seq in ("[A", "[B"):
            return seq
        return None
