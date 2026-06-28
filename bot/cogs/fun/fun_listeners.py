"""Listeners cog for fun events.

Contains listeners for user messages (handles "quoi" str)
and reaction emojis (handles reaction emoji of quote feature).

© by hassanpacary
"""

# --- Forward references ---
from __future__ import annotations

# --- Standard library ---
import re
from typing import TYPE_CHECKING

# --- Third-party ---
import discord
from discord.ext import commands

# --- Internal ---
from bot.cogs.fun import fun_config
from bot.config import regex_config
from bot.services.fun import fun_service, quote_service

if TYPE_CHECKING:
    from bot.core import bot as b


class FunListeners(commands.Cog):
    """Cog containing passive fun listeners.

    Attributes:
        bot: The custom Discord bot instance.
    """

    def __init__(self, bot: b.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """Listens for received messages.

        Replies 'feur' if the message content matches the 'quoi' pattern.

        Args:
            message: The incoming Discord message.
        """
        if message.author.bot:
            return

        if re.match(pattern=regex_config.QUOI_FEUR, string=message.content):
            await fun_service.handle_quoi_message(message=message)

    @commands.Cog.listener()
    async def on_raw_reaction_add(
            self,
            payload: discord.RawReactionActionEvent,
    ) -> None:
        """Listen for added reactions.

        Quotes a message in the quote channel when the configured reaction
        emoji is added.

        Args:
            payload: The reaction event payload.
        """
        if payload.emoji.name != fun_config.Quote.REACTION_FOR_QUOTE:
            return

        await quote_service.quote_user_by_reaction(bot=self.bot, payload=payload)
