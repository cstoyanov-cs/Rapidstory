import sys
import logging
from datetime import datetime

from .rapidstory_full import RapidStoryFull
from .rapidstory_inline import RapidStoryInline


def setup_logging(debug: bool = False):
    """Configure le logging dans un fichier /tmp/ avec niveau DEBUG si activé."""
    log_file = f"/tmp/rapidstory_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.ERROR,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stderr),  # Backup sur stderr
        ],
    )
    return log_file


def run_full_mode(debug: bool):
    """Lance le mode full-screen (Ctrl+R)."""
    log_file = setup_logging(debug)
    logger = logging.getLogger(__name__)
    logger.info("Debug: Initialisation RapidStoryFull...")

    try:
        app = RapidStoryFull()
        logger.info("Debug: Lancement run()...")
        result = app.run()

        if result:
            command, execute_directly = result
            _output_command(command, execute_directly)
            logger.info(f"Debug: Commande sélectionnée : {command}")
        else:
            logger.info("Debug: Aucune commande sélectionnée.")

    except Exception:
        logger.error("Erreur en mode full:", exc_info=True)
        sys.exit(1)
    finally:
        logger.info(f"Debug: Logs écrits dans {log_file}")


def run_inline_mode(debug: bool):
    """Lance le mode inline (Ctrl+Up)."""
    log_file = setup_logging(debug)
    logger = logging.getLogger(__name__)
    logger.info("Debug: Initialisation RapidStoryInline...")

    try:
        app = RapidStoryInline()
        logger.info("Debug: Lancement run()...")
        result = app.run()

        if result:
            command, execute_directly = result
            _output_command(command, execute_directly)
            logger.info(f"Debug: Commande sélectionnée : {command}")
        else:
            logger.info("Debug: Aucune commande sélectionnée.")

    except Exception:
        logger.error("Erreur en mode inline:", exc_info=True)
        sys.exit(1)
    finally:
        logger.info(f"Debug: Logs écrits dans {log_file}")


def _output_command(command: str, execute_directly: bool):
    """Affiche la commande dans le format attendu par bash."""
    if execute_directly:
        print(f"{command}|EXECUTE|")
    else:
        print(command)


def main():
    """Point d'entrée principal."""
    debug = "--debug" in sys.argv
    if len(sys.argv) > 1 and sys.argv[1] == "--inline":
        logging.info("Debug: Mode inline sélectionné.")
        run_inline_mode(debug)
    else:
        logging.info("Debug: Mode full sélectionné.")
        run_full_mode(debug)


if __name__ == "__main__":
    main()
