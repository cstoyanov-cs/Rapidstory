from typing import Protocol, Optional


class UIProtocol(Protocol):
    """
    Contrat d'interface pour les UI RapidStory.

    Protocol = duck typing avec vérification de type statique.
    """

    def setup(self) -> None:
        """Configure l'UI."""
        ...

    def cleanup(self) -> None:
        """Restaure l'état original."""
        ...

    def render(self, *args, **kwargs) -> None:
        """Affiche l'interface."""
        ...

    def wait_for_input(self) -> str:
        """Attend une touche utilisateur."""
        ...

    def handle_escape(self) -> Optional[str]:
        """Gère la séquence d'échappement."""
        ...
