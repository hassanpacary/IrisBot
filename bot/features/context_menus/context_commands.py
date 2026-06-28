"""Context menus commands.

Contains context commands for quote a specific user with the context menu.
Context menu commands appear when a user right-clicks a message or user.

© by hassanpacary
"""

# --- Standard library ---
import logging

# --- Third-party ---
import discord
from discord import app_commands

# --- Internal ---
from bot.cogs.fun import fun_config
from bot.services.fun import quote_service


@app_commands.context_menu(name=fun_config.Quote.CONTEXT_MENU)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def quote_context(
        interaction: discord.Interaction,
        message: discord.Message,
) -> None:
    """Quotes a message via the right-click context menu.

    Args:
        interaction: The Discord interaction context.
        message: The target message to quote.
    """
    logging.info(
        "%s used quote context menu command on a message",
        interaction.user.name,
    )
    await quote_service.quote_user_by_context(interaction=interaction, message=message)
