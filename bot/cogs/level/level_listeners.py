"""Listener cog for level events.

contains listeners for user messages (rewarded XP).

© by hassanpacary
"""

# --- Forward references ---
from __future__ import annotations

# --- Standard library ---
from typing import TYPE_CHECKING

# --- Third-party ---
import discord
from discord.ext import commands

# --- Internal ---
from bot.services.level import experience_service

if TYPE_CHECKING:
    from bot.core import bot as b



class LevelListeners(commands.Cog):
    """Cog containing passive level listeners.

    Attributes:
        bot: The custom Discord bot instance.
    """

    def __init__(self, bot: b.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """Listen for received message.

        Granting random amount of XP to the message author on each message.

        Args:
            message: The incoming Discord message.
        """
        if message.author.bot:
            return

        await experience_service.grant_xp_on_message(
            message=message,
            db=self.bot.levels_db,
        )
