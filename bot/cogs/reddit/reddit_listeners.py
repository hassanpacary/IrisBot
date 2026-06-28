"""Listener cog for Reddit events.

Contains listeners for user messages (handles reddit url).

© by hassanpacary
"""

# --- Forward references ---
from __future__ import annotations

import re
# --- Standard library ---
from typing import TYPE_CHECKING

# --- Third-party ---
import discord
from discord.ext import commands

from bot.config import regex_config
# --- Internal ---
from bot.services.reddit import reddit_service

if TYPE_CHECKING:
    from bot.core import bot as b


class RedditListeners(commands.Cog):
    """Cog containing passive reddit listeners.

    Attributes:
        bot: The custom Discord bot instance.
    """

    def __init__(self, bot: b.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """Listen for received message.

        Detects Reddit URL in messages and sends improved embed for Reddit post,
        followed by all medias of the post (videos, pictures, YouTube videos).

        Args:
            message: The incoming Discord message.
        """
        if message.author.bot:
            return

        matched_object = re.search(
            pattern=regex_config.REDDIT_URL,
            string=message.content
        )

        if matched_object:
            await reddit_service.handle_reddit_url_message(
                message=message,
                url=matched_object.group(0),
            )
