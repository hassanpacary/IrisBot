"""Commands cog for social slash commands.

Contains commands for display guild member avatar, choose custom color and
display member profile.

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
from discord.utils import MISSING

# --- Internal ---
from bot.cogs.social import social_config
from bot.services.social import color_service, profile_service, social_service

if TYPE_CHECKING:
    from bot.core import bot as b


class SocialCommands(commands.Cog):
    """Cog containing social slash commands.

    Attributes:
        bot: The custom Discord bot instance.
    """

    def __init__(self, bot: b.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name=social_config.Avatar.NAME,
        description=social_config.Avatar.DESCRIPTION,
    )
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def avatar_command(
        self,
        interaction: discord.Interaction,
        user: discord.User,
    ) -> None:
        """Responds to avatar slash command.

        Displaying a user's avatar. If no user is specified,
        displays the interaction author's avatar.

        Args:
            interaction: The Discord interaction context.
            user: The target Discord user (defaults to MISSING (self)).
        """
        logging.info(
            "%s used /avatar slash command for %s",
            interaction.user.name,
            user.name,
        )
        await social_service.retrieve_avatar(interaction=interaction, user=user)

    @app_commands.command(
        name=social_config.Color.NAME,
        description=social_config.Color.DESCRIPTION,
    )
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def color_command(
        self,
        interaction: discord.Interaction,
        name: str,
        color: str,
    ) -> None:
        """Responds to color slash command.

         Assigning a custom color role to the user.

        Args:
            interaction: The Discord interaction context.
            name: The name of the color role to assign (required).
            color: The hex value of the color (e.g. #FF5733) (required).
        """
        logging.info(
            "%s used /color slash command with role '%s' (%s)",
            interaction.user.name,
            name,
            color,
        )
        await color_service.check_ability_of_use_color_command(
            interaction=interaction,
            color_db=self.bot.colors_db,
            level_db=self.bot.levels_db,
            role_name=name,
            hex_value=color,
        )

    @app_commands.command(
        name=social_config.Profile.NAME,
        description=social_config.Profile.DESCRIPTION,
    )
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def profile_command(
        self,
        interaction: discord.Interaction,
        user: discord.User = MISSING,
    ) -> None:
        """Responds to profile slash command.

        Displaying a user's profile, if no user is specified,
        displays the interaction author's profile.

        Args:
            interaction: The Discord interaction context.
            user: The target Discord user (defaults to MISSING (self)).
        """
        target = user if user is not MISSING else interaction.user
        logging.info(
            "%s used /profile slash command for %s",
            interaction.user.name,
            target.name,
        )
        await profile_service.display_profile(
            interaction=interaction,
            db=self.bot.levels_db,
            user=target,
        )
