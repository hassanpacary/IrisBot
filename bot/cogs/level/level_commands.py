"""Commands cog for level slash commands.

Contains command for display guild leaderboard.

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
from bot.cogs.level import level_config
from bot.services.level import leaderboard_service

if TYPE_CHECKING:
    from bot.core import bot as b



class LevelCommands(commands.Cog):
    """Cog containing level slash cogs.

    Attributes:
        bot: The custom Discord bot instance.
    """

    def __init__(self, bot: b.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name=level_config.Leaderboard.NAME,
        description=level_config.Leaderboard.DESCRIPTION,
    )
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def leaderboard_command(
        self,
        interaction: discord.Interaction,
    ) -> None:
        """Responds to leaderboard slash command.

        Displaying the XP and level rankings in the guild.

        Args:
            interaction: The Discord interaction context.
        """
        logging.info(
            "%s used /leaderboard slash command",
            interaction.user.name,
        )
        await leaderboard_service.display_leaderboard(
            interaction=interaction,
            db=self.bot.levels_db
        )
