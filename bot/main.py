"""Entrypoint of the Discord bot.

Initializes logging, loads environment variables, starts the bot,
and ensures clean shutdown of all async resources on exit.

© by hassanpacary
"""


# --- Standard library ---
import asyncio
import logging

# --- Internal ---
from bot.core import bot as b, environment
from bot.core.setup_logging import setup_logging


async def _run() -> None:
    """Initializes and starts the Discord bot.

    Ensures that bot connection are closed cleanly even if an exception
    occurs during startup or runtime.
    """
    environment.load_env()
    bot = b.Bot()

    try:
        await bot.start(environment.get_env_var("DISCORD_TOKEN"))
    finally:
        await bot.close()


def _main() -> None:
    """Sets up logging and runs the bot event loop.

    Raises:
        KeyboardInterrupt: Graceful manual stop.
        OSError: Fatal system-level failures.
    """
    setup_logging()

    try:
        asyncio.run(_run())
    except KeyboardInterrupt:
        logging.info("Bot stopped manually")
    except OSError as e:
        logging.critical("OS error: %s", e, exc_info=True)


if __name__ == "__main__":
    _main()
