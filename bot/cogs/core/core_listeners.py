"""Listener cog for core events.

Contains listeners for when the bot is ready, resumed, closed,
and when an unhandled exceptions are raised (logs).

© by hassanpacary
"""

# --- Forward references ---
from __future__ import annotations

# --- Standard library ---
import logging
from typing import TYPE_CHECKING

# --- Third-party ---
from discord.ext import commands

# --- Internal ---
if TYPE_CHECKING:
    from bot.core import bot as b


class CoreListeners(commands.Cog):
    """Cog containing passive bot core listeners.

    Attributes:
        bot: The custom Discord bot instance.
    """

    def __init__(self, bot: b.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_close(self) -> None:
        """Listen for bot status.

        Logs a message when the bot shuts down.
        """
        logging.info("Disconnecting with success !")

    @commands.Cog.listener()
    async def on_error(self, event: str, *_args, **_kwargs) -> None:
        """Listens for exceptions raised by the bot.

        Logs unhandled exceptions.

        Args:
            event: The name of the event that raised the exception.
        """
        logging.exception("Unhandled error by the bot %s.", event)

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Listen for bot status.

        Logs a message when bot is ready to use.
        """
        logging.info("Ready steady go !")

    @commands.Cog.listener()
    async def on_resumed(self) -> None:
        """Listen for bot status.

        Logs a message when the bot successfully reconnects.
        """
        logging.info("Resumed with success !")
