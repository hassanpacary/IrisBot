"""Configures the bot logging system.

Sets up two handlers:
- A rotating file handler writing to logs/bot.log (max 5 MB, 3 backups).
- A stream handler writing to stdout for real-time console output.

Called before bot startup.

© by hassanpacary
"""

# --- Standard library ---
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# --- Constants ---
_LOG_DIR = Path("logs")
_LOG_FILE = _LOG_DIR / "bot.log"
_LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
_LOG_DATE_FORMAT = "%d.%m.%Y %H:%M:%S"
_LOG_MAX_BYTES = 5 * 1024 * 1024  # 5 MB per file
_LOG_BACKUP_COUNT = 3             # bot.log, bot.log.1, bot.log.2


def setup_logging(level: int = logging.INFO) -> None:
    """Configures root logger with a rotating file handler and stdout stream.

    Creates the logs/ directory if it does not already exist. Uses a
    RotatingFileHandler to prevent unbounded log file growth.

    Args:
        level: The minimum logging level to capture. Defaults to logging.INFO.
    """
    _LOG_DIR.mkdir(exist_ok=True)

    logging.basicConfig(
        level=level,
        format=_LOG_FORMAT,
        datefmt=_LOG_DATE_FORMAT,
        handlers=[
            RotatingFileHandler(
                _LOG_FILE,
                maxBytes=_LOG_MAX_BYTES,
                backupCount=_LOG_BACKUP_COUNT,
                encoding="utf-8",
            ),
            logging.StreamHandler(sys.stdout),
        ],
    )
