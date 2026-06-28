"""Admin-only commands cog for guild slash commands.

Contains command for purge a channel.

© by hassanpacary
"""

# --- Forward references ---
from __future__ import annotations

# --- Standard library ---
import logging
from typing import TYPE_CHECKING

# --- Third-party ---
import discord
from discord import app_commands
from discord.ext import commands

# --- Internal ---
from bot.cogs.guild import guild_config
from bot.services.guild import guild_admin_service

if TYPE_CHECKING:
    from bot.core import bot as b


@app_commands.default_permissions(administrator=True)
class GuildAdminCommands(commands.Cog):
    """Cog containing admin-only guild moderation slash commands.

    Attributes:
        bot: The custom Discord bot instance.
    """

    def __init__(self, bot: b.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name=guild_config.AdminCommands.Purge.NAME,
        description=guild_config.AdminCommands.Purge.DESCRIPTION,
    )
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def purge_command(
        self,
        interaction: discord.Interaction,
        amount: int = 1,
    ) -> None:
        """Responds to purge slash commands.

        Deleting a given number of messages in the current channel.
        By default, it deletes only one message in the current channel.

        Args:
            interaction: The Discord interaction context.
            amount: The number of messages to delete (Defaults to 1).
        """
        logging.info(
            "%s used /purge slash command to delete %s message(s)",
            interaction.user.name,
            amount,
        )
        await guild_admin_service.purge(interaction=interaction, amount=amount)
