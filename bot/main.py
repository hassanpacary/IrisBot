"""
bot/main.py
© by hassanpacary

Entrypoint of the Discord bot
"""

# --- Imports ---
import asyncio
import logging

# --- Bot modules ---
from bot.core.config_loader import RUN_BANNER, INTERUPT_BANNER
from bot.core.setup_bot import Bot
from bot.core.environment import load_env, get_env_var
from bot.core.setup_logging import setup_logging
from bot.utils.aiohttp_client import aiohttp_shutdown


# ███╗   ███╗ █████╗ ██╗███╗   ██╗
# ████╗ ████║██╔══██╗██║████╗  ██║
# ██╔████╔██║███████║██║██╔██╗ ██║
# ██║╚██╔╝██║██╔══██║██║██║╚██╗██║
# ██║ ╚═╝ ██║██║  ██║██║██║ ╚████║
# ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝


async def run() -> None:
    """Initialize and start the Discord bot"""
    load_env()
    bot = Bot()

    try:
        await bot.start(get_env_var("DISCORD_TOKEN"))
    finally:
        await aiohttp_shutdown()
        await bot.close()


def main() -> None:
    """Main func. Setup logging config and run the Discord bot"""
    setup_logging()
    logging.info(RUN_BANNER)

    try:
        asyncio.run(run())

    except KeyboardInterrupt:
        logging.info("-- Bot stopped manually.")
        logging.info(INTERUPT_BANNER)

    except OSError as e:
        logging.critical("Erreur OS : %s", e, exc_info=True)

    except asyncio.CancelledError:
        logging.info("Tâches annulées proprement.")


if __name__ == "__main__":
    main()
