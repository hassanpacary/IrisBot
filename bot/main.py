"""
bot/main.py
© by hassanpacary

Entrypoint of the Discord bot.
"""

# --- Imports ---
import asyncio
import logging

# --- Bot modules ---
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
    run_banner = r"""
    ██╗      ██████╗  █████╗ ██████╗ ██╗███╗   ██╗ ██████╗                      
    ██║     ██╔═══██╗██╔══██╗██╔══██╗██║████╗  ██║██╔════╝                      
    ██║     ██║   ██║███████║██║  ██║██║██╔██╗ ██║██║  ███╗                     
    ██║     ██║   ██║██╔══██║██║  ██║██║██║╚██╗██║██║   ██║                     
    ███████╗╚██████╔╝██║  ██║██████╔╝██║██║ ╚████║╚██████╔╝    ██╗    ██╗    ██╗
    ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝     ╚═╝    ╚═╝    ╚═╝                                                  
    """

    # Config
    setup_logging()
    load_env()

    # Start bot
    bot = Bot()

    logging.info(run_banner)
    await bot.start(get_env_var("DISCORD_TOKEN"))


def main() -> None:
    """Entrypoint of the bot (sync wrapper)."""
    on_disconnect_banner = r"""
    ██████╗ ██╗███████╗ ██████╗ ██████╗ ███╗   ██╗███╗   ██╗███████╗ ██████╗████████╗███████╗██████╗ 
    ██╔══██╗██║██╔════╝██╔════╝██╔═══██╗████╗  ██║████╗  ██║██╔════╝██╔════╝╚══██╔══╝██╔════╝██╔══██╗
    ██║  ██║██║███████╗██║     ██║   ██║██╔██╗ ██║██╔██╗ ██║█████╗  ██║        ██║   █████╗  ██║  ██║
    ██║  ██║██║╚════██║██║     ██║   ██║██║╚██╗██║██║╚██╗██║██╔══╝  ██║        ██║   ██╔══╝  ██║  ██║
    ██████╔╝██║███████║╚██████╗╚██████╔╝██║ ╚████║██║ ╚████║███████╗╚██████╗   ██║   ███████╗██████╔╝
    ╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝ ╚═════╝   ╚═╝   ╚══════╝╚═════╝                                                                                                                                          
    """

    try:
        asyncio.run(run())

    except KeyboardInterrupt:
        logging.info("-- Bot stopped manually.")
        logging.info(on_disconnect_banner)
    except Exception as e:
        logging.critical("Fatal error in main: %s", e, exc_info=True)
        logging.info(on_disconnect_banner)


if __name__ == "__main__":
    main()
