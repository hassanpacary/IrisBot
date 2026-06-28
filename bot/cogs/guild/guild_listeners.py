"""Listeners cog for guild events.

Contains listeners for user join (welcome messager), user remove (goodbye message),
user message delete or edited (logs).

© by hassanpacary
"""

# --- Forward references ---
from __future__ import annotations

# --- Standard library ---
import logging
from typing import TYPE_CHECKING

# --- Third-party ---
import discord
from discord.ext import commands

# --- Internal ---
from bot.services.guild import guild_service

if TYPE_CHECKING:
    from bot.core import bot as b


class GuildListeners(commands.Cog):
    """Cog containing passive guild listeners.

    Attributes:
        bot: The custom Discord bot instance.
    """

    def __init__(self, bot: b.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, user: discord.User) -> None:
        """Listen for user joins the server.

        Sends a welcome message when a new user joins the server.

        Args:
            user: The discord User who joined the guild.
        """
        logging.info("New user joined: %s", user.name)
        await guild_service.welcome(bot=self.bot, user=user)

    @commands.Cog.listener()
    async def on_member_remove(self, user: discord.User) -> None:
        """Listen for user leaves the server.

        Sends a goodbye message when a user leaves the server.

        Args:
            user: The Discord user who left the guild.
        """
        logging.info("User left server: %s", user.name)
        await guild_service.goodbye(bot=self.bot, user=user)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message) -> None:
        """Listen for deleted message.

        Logs a message when it is deleted.

        Args:
            message: The deleted Discord message.
        """
        if message.author.bot:
            return

        logging.info(
            "Message deleted in #%s by %s",
            message.channel,
            message.author.name,
        )
        await guild_service.log_deleted_message(bot=self.bot, message=message)

    @commands.Cog.listener()
    async def on_message_edit(
        self,
        message_before: discord.Message,
        message_after: discord.Message,
    ) -> None:
        """Listen for edited message.

        Logs a message when it is edited.

        Args:
            message_before: The message content before the edit.
            message_after: The message content after the edit.
        """
        if message_before.author.bot:
            return

        logging.info(
            "Message edited in #%s by %s",
            message_before.channel,
            message_before.author.name,
        )
        await guild_service.log_edited_message(
            bot=self.bot,
            message_before=message_before,
            message_after=message_after,
        )
