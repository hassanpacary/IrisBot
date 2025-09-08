"""
bot/core/setup_logging.py
© by hassanpacary

Configuration of the logs.
"""

# --- Imports ---
import logging
import sys
from pathlib import Path


# ██╗      ██████╗  ██████╗  ██████╗ ██╗███╗   ██╗ ██████╗
# ██║     ██╔═══██╗██╔════╝ ██╔════╝ ██║████╗  ██║██╔════╝
# ██║     ██║   ██║██║  ███╗██║  ███╗██║██╔██╗ ██║██║  ███╗
# ██║     ██║   ██║██║   ██║██║   ██║██║██║╚██╗██║██║   ██║
# ███████╗╚██████╔╝╚██████╔╝╚██████╔╝██║██║ ╚████║╚██████╔╝
# ╚══════╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝


def setup_logging(level: int = logging.INFO) -> None:
    """Configure global logging for the bot."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%d.%m.%Y %H:%M:%S",
        handlers=[
            logging.FileHandler(log_dir / "bot.log", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )
