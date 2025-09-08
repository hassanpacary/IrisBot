"""
bot/utils/cogs_factory.py
© by hassanpacary

Utility functions for factor discord commands
"""

# --- Imports ---
import importlib
import logging
import pkgutil

# --- Bot modules ---
import bot.cogs as cogs


# ██╗      ██████╗  █████╗ ██████╗
# ██║     ██╔═══██╗██╔══██╗██╔══██╗
# ██║     ██║   ██║███████║██║  ██║
# ██║     ██║   ██║██╔══██║██║  ██║
# ███████╗╚██████╔╝██║  ██║██████╔╝
# ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝


async def load_all_cogs(bot) -> None:
    """Discover and load all cogs from the `bot.cogs` package."""
    for _, cog_name, _ in pkgutil.iter_modules(cogs.__path__):

        # --- Add cog and cog commands to the tree commands ---
        try:
            cog = importlib.import_module(f"bot.cogs.{cog_name}")
            await cog.setup(bot)
            logging.info(f"-- Loaded cog '{cog_name}' successfully.")

        except Exception as e:
            logging.exception(f"Failed to setup cog '{cog_name}': {e}")
