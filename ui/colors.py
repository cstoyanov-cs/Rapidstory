from typing import Optional


class ColorFormatter:
    """
    Convertit les paramètres de couleur en codes ANSI.

    Supporte : couleurs nommées, codes 256, RGB hex, RGB décimal.
    Responsabilité unique : transformation couleur → ANSI.
    """

    COLORS = {
        "black": "30",
        "red": "31",
        "green": "32",
        "yellow": "33",
        "blue": "34",
        "magenta": "35",
        "cyan": "36",
        "white": "37",
    }

    ATTRIBUTES = {"bold": "1", "dim": "2", "underline": "4", "reverse": "7"}

    @staticmethod
    def _parse_color(color: str, is_bg: bool) -> str:
        """
        Parse une couleur et retourne le code ANSI correspondant.

        Args:
            color: Couleur (nom, code, hex, rgb)
            is_bg: True si couleur de fond, False si premier plan

        Returns:
            Code ANSI formaté
        """
        if isinstance(color, int):
            color = str(color)

        prefix_rgb = "48;2" if is_bg else "38;2"
        prefix_256 = "48;5" if is_bg else "38;5"

        if color in ColorFormatter.COLORS:
            code = ColorFormatter.COLORS[color]
            if is_bg:
                return str(int(code) + 10)
            return code

        if color.startswith("#"):
            hex_color = color[1:]
            if len(hex_color) == 3:
                hex_color = "".join([c * 2 for c in hex_color])
            if len(hex_color) == 6:
                try:
                    r = int(hex_color[0:2], 16)
                    g = int(hex_color[2:4], 16)
                    b = int(hex_color[4:6], 16)
                    return f"{prefix_rgb};{r};{g};{b}"
                except ValueError:
                    pass

        if "," in color:
            try:
                parts = color.split(",")
                if len(parts) == 3:
                    r, g, b = map(int, parts)
                    if all(0 <= c <= 255 for c in [r, g, b]):
                        return f"{prefix_rgb};{r};{g};{b}"
            except ValueError:
                pass

        return f"{prefix_256};{color}"

    @staticmethod
    def format(fg: Optional[str], bg: Optional[str], attr: Optional[str]) -> str:
        """
        Crée un code ANSI complet à partir des paramètres.

        Args:
            fg: Couleur avant-plan (None = défaut)
            bg: Couleur arrière-plan (None = défaut)
            attr: Attribut (bold, dim, etc.)

        Returns:
            Séquence ANSI complète ou chaîne vide
        """
        codes = []

        if attr and attr in ColorFormatter.ATTRIBUTES:
            codes.append(ColorFormatter.ATTRIBUTES[attr])

        if fg:
            codes.append(ColorFormatter._parse_color(fg, False))

        if bg:
            codes.append(ColorFormatter._parse_color(bg, True))

        if codes:
            return f"\033[{';'.join(codes)}m"

        return ""

    @staticmethod
    def reset() -> str:
        """Retourne le code ANSI de réinitialisation."""
        return "\033[0m"
