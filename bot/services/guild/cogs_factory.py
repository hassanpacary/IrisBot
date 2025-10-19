"""
bot/services/guild/cogs_factory.py
© by hassanpacary

Factor discord commands
"""

# --- Imports ---
import importlib
import logging
import pkgutil

# --- Third party imports ---
from discord.ext import commands
from discord.ext.commands import ExtensionNotLoaded, ExtensionFailed

# --- Bot modules ---
from bot import cogs


# ██╗      ██████╗  █████╗ ██████╗
# ██║     ██╔═══██╗██╔══██╗██╔══██╗
# ██║     ██║   ██║███████║██║  ██║
# ██║     ██║   ██║██╔══██║██║  ██║
# ███████╗╚██████╔╝██║  ██║██████╔╝
# ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝


async def load_cogs(ctx: commands.Bot):
    """Load all cogs from the `bot.cogs` package."""
    for _, cog_name, _ in pkgutil.iter_modules(cogs.__path__):

        # Add cog and cog commands to the tree commands
        try:
            cog = importlib.import_module(f"bot.cogs.{cog_name}")
            await ctx.load_extension(cog.__name__)
            logging.info(
                "-- Loaded cog '%s' successfully.",
                cog_name
            )

        except (ExtensionNotLoaded, ExtensionFailed) as e:
            logging.exception(
                "Failed to load cog '%s': %s",
                cog_name,
                e
            )


# ██████╗ ███████╗██╗      ██████╗  █████╗ ██████╗
# ██╔══██╗██╔════╝██║     ██╔═══██╗██╔══██╗██╔══██╗
# ██████╔╝█████╗  ██║     ██║   ██║███████║██║  ██║
# ██╔══██╗██╔══╝  ██║     ██║   ██║██╔══██║██║  ██║
# ██║  ██║███████╗███████╗╚██████╔╝██║  ██║██████╔╝
# ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝


async def reload_cogs(ctx: commands.Bot):
    """Reload all cogs from the `bot.cogs` package."""
    for _, cog_name, _ in pkgutil.iter_modules(cogs.__path__):

        # Re-add cog and cog commands to the tree commands
        try:
            cog = importlib.import_module(f"bot.cogs.{cog_name}")
            await ctx.reload_extension(cog.__name__)
            logging.info(
                "-- reloaded cog '%s' successfully.",
                cog_name
            )

        except (ExtensionNotLoaded, ExtensionFailed) as e:
            logging.exception(
                "Failed to reload cog '%s': %s",
                cog_name,
                e
            )


# ██╗   ██╗███╗   ██╗██╗      ██████╗  █████╗ ██████╗
# ██║   ██║████╗  ██║██║     ██╔═══██╗██╔══██╗██╔══██╗
# ██║   ██║██╔██╗ ██║██║     ██║   ██║███████║██║  ██║
# ██║   ██║██║╚██╗██║██║     ██║   ██║██╔══██║██║  ██║
# ╚██████╔╝██║ ╚████║███████╗╚██████╔╝██║  ██║██████╔╝
#  ╚═════╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝


async def unload_cogs(ctx: commands.Bot):
    """Unload all cogs from the `bot.cogs` package."""
    for _, cog_name, _ in pkgutil.iter_modules(cogs.__path__):

        # Remove cog and cog commands to the tree commands
        try:
            cog = importlib.import_module(f"bot.cogs.{cog_name}")
            await ctx.unload_extension(cog.__name__)
            logging.info(
                "-- Unloaded cog '%s' successfully.",
                cog_name
            )

        except (ExtensionNotLoaded, ExtensionFailed) as e:
            logging.exception(
                "Failed to unload cog '%s': %s",
                cog_name,
                e
            )
