"""Admin-only commands cog for level slash commands.

Contains commands for give xp to a specific user and reset xp/level to a specific user.

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
from bot.services.level import experience_admin_service

if TYPE_CHECKING:
    from bot.core import bot as b


@app_commands.default_permissions(administrator=True)
class LevelAdminCommands(commands.Cog):
    """Cog containing admin-only level slash cogs.

    Attributes:
        bot: The custom Discord bot instance.
    """

    def __init__(self, bot: b.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name=level_config.AdminCommands.Give.NAME,
        description=level_config.AdminCommands.Give.DESCRIPTION,
    )
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def give_command(
        self,
        interaction: discord.Interaction,
        amount: int,
        user: discord.User,
    ) -> None:
        """Responds to give slash command.

        Granting specific amount of XP to a target Discord user.

        Args:
            interaction: The Discord interaction context.
            amount: The amount of XP to grant (required).
            user: The target Discord user to receive the XP (required).
        """
        logging.info(
            "%s used /give slash command for %s (%s XP)",
            interaction.user.name,
            user.name,
            amount,
        )
        await experience_admin_service.grant_xp_by_admin(
            interaction=interaction,
            db=self.bot.levels_db,
            amount=amount,
            user=user,
        )

    @app_commands.command(
        name=level_config.AdminCommands.Reset.NAME,
        description=level_config.AdminCommands.Reset.DESCRIPTION,
    )
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def reset_command(
        self,
        interaction: discord.Interaction,
        user: discord.User,
    ) -> None:
        """Responds to reset slash command.

        Resetting the XP and level of target Discord user.

        Args:
            interaction: The Discord interaction context.
            user: The target Discord user whose level will be reset (required).
        """
        logging.info(
            "%s used /reset slash command for %s",
            interaction.user.name,
            user.name,
        )
        await experience_admin_service.reset_user_level(
            interaction=interaction,
            db=self.bot.levels_db,
            user=user,
        )
