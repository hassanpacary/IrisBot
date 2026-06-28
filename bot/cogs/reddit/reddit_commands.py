"""Commands cog for Reddit slash commands.

Contains commands for display improved post embed.

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
from bot.cogs.reddit import reddit_config
from bot.services.reddit import reddit_service

if TYPE_CHECKING:
    from bot.core import bot as b


class RedditCommands(commands.Cog):
    """Cog containing Reddit slash cogs.

    Attributes:
        bot: The custom Discord bot instance.
    """

    def __init__(self, bot: b.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name=reddit_config.Waf.NAME,
        description=reddit_config.Waf.DESCRIPTION,
    )
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def waf_command(
        self,
        interaction: discord.Interaction,
        url: str,
    ) -> None:
        """Responds to waf slash command.

        Sending improved embed for a Reddit post URL,
        followed by all medias of the post (videos, pictures, YouTube videos).

        Args:
            interaction: The Discord interaction context.
            url: The Reddit post URL to embed (required).
        """
        logging.info(
            "%s used /waf slash command with url: %s",
            interaction.user.name,
            url,
        )
        await reddit_service.handle_reddit_url(interaction=interaction, url=url)
