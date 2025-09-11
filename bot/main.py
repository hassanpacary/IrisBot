"""
bot/main.py
© by hassanpacary

Entrypoint of the Discord bot.
"""
import asyncio
# --- Imports ---
import logging

# --- Bot modules ---
from bot.core.config_loader import RUN_BANNER, INTERUPT_BANNER
from bot.core.setup_bot import Bot
from bot.core.environment import load_env, get_env_var
from bot.core.setup_logging import setup_logging


# ███╗   ███╗ █████╗ ██╗███╗   ██╗
# ████╗ ████║██╔══██╗██║████╗  ██║
# ██╔████╔██║███████║██║██╔██╗ ██║
# ██║╚██╔╝██║██╔══██║██║██║╚██╗██║
# ██║ ╚═╝ ██║██║  ██║██║██║ ╚████║
# ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝

async def run() -> None:
    """Initialize and start the Discord bot."""
    load_env()
    bot = Bot()
    await bot.start(get_env_var("DISCORD_TOKEN"))

def main() -> None:
    """Entrypoint of the bot (sync wrapper)."""
    setup_logging()
    logging.info(RUN_BANNER)

    try:
        asyncio.run(run())

    except KeyboardInterrupt:
        logging.info("-- Bot stopped manually.")
        logging.info(INTERUPT_BANNER)
    except Exception as e:
        logging.critical("Fatal error in main: %s", e, exc_info=True)
        logging.info(INTERUPT_BANNER)


if __name__ == "__main__":
    main()
