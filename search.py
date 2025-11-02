from typing import List, Tuple, Optional
import logging
from rapidfuzz import fuzz, process  # pip install rapidfuzz (rapide, C++ backend)


class QueryParser:
    """
    Parse les requêtes et gère le mode recherche avec délimiteurs.

    Principe : Entre délimiteurs (ex: '8000'), les chiffres sont recherchés.
    Hors délimiteurs, les chiffres sélectionnent des commandes.
    """

    def __init__(self, delimiter: str = "'"):
        """
        Args:
            delimiter: Caractère délimiteur (apostrophe par défaut)
        """
        self.delimiter = delimiter

    def is_in_search_mode(self, query: str) -> bool:
        """
        Vérifie si la query est en mode recherche (nombre impair de délimiteurs).

        Args:
            query: La requête à analyser

        Returns:
            True si en mode recherche, False sinon
        """
        count = query.count(self.delimiter)
        return count % 2 == 1

    def get_search_text(self, query: str) -> str:
        """
        Extrait le texte de recherche sans les délimiteurs.

        Args:
            query: La requête brute (avec délimiteurs)

        Returns:
            Texte nettoyé pour la recherche
        """
        return query.replace(self.delimiter, "")


class SearchEngine:
    """Moteur de recherche centralisé. Gère parsing ET recherche."""

    def __init__(
        self, threshold: float = 0.5, query_parser: Optional[QueryParser] = None
    ):
        """
        Args:
            threshold: Seuil minimum pour la recherche floue (0.0 à 1.0)
            query_parser: Parser pour gérer les délimiteurs (optionnel)
        """
        self.threshold = threshold
        self.query_parser = query_parser if query_parser is not None else QueryParser()
        self.logger = logging.getLogger(__name__)

    def search(self, query: str, commands: List[str], limit: int) -> List[str]:
        """
        Recherche des commandes selon une requête.

        GÈRE AUTOMATIQUEMENT le nettoyage de la query (délimiteurs).

        Stratégie hybride optimisée :
        1. Priorise les correspondances exactes (sous-chaîne)
        2. Complète avec recherche floue rapide (rapidfuzz)

        Args:
            query: La chaîne de recherche (peut contenir délimiteurs)
            commands: Liste des commandes à parcourir
            limit: Nombre maximum de résultats

        Returns:
            Liste des commandes correspondantes, triées par pertinence
        """
        # Nettoie automatiquement la query (enlève délimiteurs)
        clean_query = self.query_parser.get_search_text(query)

        if not clean_query:
            return commands[:limit]

        lower_query = clean_query.lower()
        scored_results = self._score_commands_optimized(lower_query, commands)

        scored_results.sort(key=lambda x: (x[0], x[1]), reverse=True)

        return [cmd for _, _, cmd in scored_results[:limit]]

    def is_in_search_mode(self, query: str) -> bool:
        """
        Vérifie si la query est en mode recherche (pour UI).

        Args:
            query: Query à vérifier

        Returns:
            True si en mode recherche
        """
        return self.query_parser.is_in_search_mode(query)

    def _score_commands_optimized(
        self, query: str, commands: List[str]
    ) -> List[Tuple[float, int, str]]:
        """
        Calcule le score de pertinence pour chaque commande (version rapide).

        Args:
            query: Requête en minuscules
            commands: Liste des commandes

        Returns:
            Liste de tuples (score, -index, commande)
        """
        scored_results: List[Tuple[float, int, str]] = []

        # Priorité 1: Matches exacts (rapide)
        exact_matches = [cmd for cmd in commands if query in cmd.lower()]
        for cmd in exact_matches:
            idx = commands.index(cmd)  # Stable pour tri
            scored_results.append((1.0, -idx, cmd))

        # Priorité 2: Fuzzy rapide avec rapidfuzz (seulement si pas assez d'exacts)
        if len(scored_results) < len(commands):
            try:
                fuzzy_matches = process.extract(
                    query,
                    [cmd.lower() for cmd in commands],
                    scorer=fuzz.ratio,
                    limit=50,
                )
                seen_cmds = {
                    s[2] for s in scored_results
                }  # Set pour O(1) check doublons
                for _, score, idx in fuzzy_matches:
                    score_norm: float = (
                        float(score) / 100.0
                    )  # Cast explicite pour Pyright
                    if score_norm >= self.threshold and score_norm < 1.0:
                        cmd = commands[idx]
                        if cmd not in seen_cmds:
                            scored_results.append((score_norm, -idx, cmd))
                            seen_cmds.add(cmd)  # Ajoute après pour éviter doublons
            except Exception as e:
                self.logger.warning(
                    f"Fallback fuzzy échoué : {e}. Utilise exacts seulement."
                )
                # Optionnel : fallback à difflib ici si besoin

        return scored_results


class FuzzyMatcher:
    """Matcher pour recherche floue uniquement (extension future)."""

    @staticmethod
    def calculate_similarity(str1: str, str2: str) -> float:
        """Calcule la similarité entre deux chaînes."""
        return fuzz.ratio(str1.lower(), str2.lower()) / 100.0

    @staticmethod
    def find_best_matches(query: str, candidates: List[str], n: int = 5) -> List[str]:
        """Trouve les n meilleures correspondances floues."""
        return [match[0] for match in process.extract(query, candidates, limit=n)]
