# ============================================================================
# PARAMÈTRES GLOBAUX
# ============================================================================

# === Historique ===
# Nombre de commandes à charger depuis ~/.bash_history
HISTORY_LOAD_LIMIT = 3000

# Taille de l'historique en mémoire (HISTSIZE dans bash)
HISTSIZE = 20000

# Taille de l'historique sur disque (HISTFILESIZE dans bash)
HISTFILESIZE = 20000

# Intervalle de surveillance du fichier d'historique (secondes)
MONITOR_INTERVAL = 30

# Fréquence d'append dans l'historique (tous les N commandes)
HISTORY_APPEND_FREQUENCY = 10


# === Chemins ===
# Base de données SQLite
DB_PATH = "~/.local/share/rapidstory/rapidstory.db"

# Fichier d'historique Bash
BASH_HISTORY_PATH = "~/.bash_history"


# === Recherche ===
# Seuil de correspondance pour la recherche floue (0.0 à 1.0)
FUZZY_SEARCH_THRESHOLD = 0.5

# Délimiteur pour mode recherche avec chiffres (ex: '8000' cherche "8000")
# Hors délimiteurs, les chiffres sélectionnent des commandes
# Changez en '"' pour utiliser des guillemets au lieu d'apostrophes
SEARCH_MODE_DELIMITER = "'"

# ============================================================================
# MODE FULL (Ctrl+R) - Interface alternate screen
# ============================================================================

# === Affichage ===
# Nombre d'entrées affichées
DISPLAY_LIMIT = 20

# Longueur maximale d'affichage d'une commande (caractères)
MAX_COMMAND_DISPLAY_LENGTH = 80

# Exécuter directement (True) ou insérer dans le prompt (False)
EXECUTE_DIRECTLY_FULL_MODE = True

# Navigation inversée (True = Haut=ancien, Bas=récent comme bash)
FULL_REVERSE_NAVIGATION = False

# Position des suggestions ("top" ou "bottom")
# top = suggestions au-dessus de la ligne active (cohérent avec reverse)
# bottom = suggestions en dessous (comportement actuel)
FULL_SUGGESTIONS_POSITION = "bottom"

# === Couleurs Mode Full ===
# Format: (fg_color, bg_color, attributes)
# fg_color/bg_color: code ANSI, int, ou None
# attributes: 'bold', 'dim', 'underline', 'reverse' ou None

# Indicateur de ligne active (→ ou □ ou autre)
FULL_ACTIVE_INDICATOR = "▎"
FULL_ACTIVE_INDICATOR_FG = "blue"
FULL_ACTIVE_INDICATOR_BG = None
FULL_ACTIVE_INDICATOR_ATTR = "bold"

# Ligne active (sélectionnée)
FULL_ACTIVE_LINE_FG = "white"  # Texte (None = couleur par défaut)
FULL_ACTIVE_LINE_BG = 33  # Fond (None = couleur par défaut)
FULL_ACTIVE_LINE_ATTR = None

# Lignes normales
FULL_NORMAL_LINE_FG = None
FULL_NORMAL_LINE_BG = None
FULL_NORMAL_LINE_ATTR = None

# Numéros de ligne (1. 2. 3. etc.)
FULL_NUMBER_FG = 252  # Gris
FULL_NUMBER_BG = None
FULL_NUMBER_ATTR = None


# ============================================================================
# MODE INLINE (Ctrl+Up) - Interface dans le terminal
# ============================================================================

# === Comportement ===
# Exécuter directement (True) ou insérer dans le prompt (False)
EXECUTE_DIRECTLY_INLINE_MODE = True

# Nombre de suggestions affichées (max 9)
INLINE_SUGGESTIONS_LIMIT = 3

# Navigation inversée (True = Haut=ancien, Bas=récent comme bash)
INLINE_REVERSE_NAVIGATION = True

# Position des suggestions ("top" ou "bottom")
# top = suggestions au-dessus de la ligne actuelle
# bottom = suggestions en dessous (comportement to
INLINE_SUGGESTIONS_POSITION = "top"

# === Couleurs Mode Inline ===

# Indicateur de commande actuelle (→ ou □ ou autre)
INLINE_CURRENT_INDICATOR = "→"
INLINE_CURRENT_INDICATOR_FG = 33
INLINE_CURRENT_INDICATOR_BG = None
INLINE_CURRENT_INDICATOR_ATTR = "bold"

# Commande actuelle (ligne 1)
INLINE_CURRENT_FG = "white"
INLINE_CURRENT_BG = 33
INLINE_CURRENT_ATTR = None

# Suggestions (lignes 2, 3, 4)
INLINE_SUGGESTION_FG = 252
INLINE_SUGGESTION_BG = None
INLINE_SUGGESTION_ATTR = None

# Numéros des suggestions (1. 2. 3.)
INLINE_NUMBER_FG = 252  # Gris
INLINE_NUMBER_BG = None
INLINE_NUMBER_ATTR = None

# Texte "[Recherche: ...]"
INLINE_SEARCH_LABEL_FG = "252"
INLINE_SEARCH_LABEL_BG = None
INLINE_SEARCH_LABEL_ATTR = None


# ============================================================================
# CODES COULEURS ANSI (référence)
# ============================================================================
# Utilisables pour les paramètres *_FG et *_BG ci-dessus
#
# Couleurs standards :
# "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"
#
# Couleurs 256 (0-255) :
# "242" (gris moyen), "237" (gris foncé), "15" (blanc brillant)
#
# Couleurs RGB Hex :
# "#5FAFFF" (bleu clair), "#FF5F87" (rose), "#87D700" (vert pomme)
# "#5AF" (format court, équivalent à #55AAFF)
#
# Couleurs RGB décimal :
# "95,175,255" (bleu clair), "255,95,135" (rose)
#
# Attributs disponibles :
# "bold", "dim", "underline", "reverse", None
#
# Exemples combinés :
# INLINE_CURRENT_FG = "#5FAFFF"      # Bleu clair en hex
# INLINE_CURRENT_BG = "237"           # Fond gris foncé
# INLINE_CURRENT_ATTR = "bold"        # En gras
# ============================================================================
