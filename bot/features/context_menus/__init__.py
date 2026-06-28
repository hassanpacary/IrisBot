"""Context menus package.

Registers the context command quote context into the bot's commands tree.

© by hassanpacary
"""

# --- Standard library ---
import logging

# --- Third-party ---
from discord.ext import commands

# --- Internal ---
from bot.features.context_menus import context_commands


async def setup(bot: commands.Bot) -> None:
    """Loads context command quote context into the bot.

    Args:
        bot: The Discord bot instance.
    """
    bot.tree.add_command(context_commands.quote_context)
    logging.info("Context menu commands loaded successfully.",)
