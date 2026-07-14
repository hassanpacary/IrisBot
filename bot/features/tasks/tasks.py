"""Background task scheduler.

Contains all recurring tasks: activity rotation, monthly quote reset,
and deals notifications.

© by hassanpacary
"""

# --- Forward references ---
from __future__ import annotations

# --- Standard library ---
import logging
from typing import TYPE_CHECKING

# --- Third-party ---
from datetime import time, timezone
from discord.ext import tasks

# --- Internal ---
from bot.cogs.fun import fun_config
from bot.services.fun import quote_fest_service
from bot.services.guild import activity_service, deals_service

if TYPE_CHECKING:
    from bot.core import bot as b


class TasksScheduler:
    """Manages and starts all bot background tasks.
    Each task is a discord.ext.tasks loop bound to this instance.

    Attributes:
        bot: The custom Discord bot instance.
    """

    def __init__(self, bot: b.Bot) -> None:
        self.bot = bot

    def start(self) -> None:
        """Starts all background tasks."""
        self.swap_activity_task.start()
        self.fest_end_task.start()
        self.check_deals_task.start()

    @tasks.loop(hours=1)
    async def check_deals_task(self) -> None:
        """Task loop every hour.

        Checks videos games stores for discounted prices
        and sends them in a Discord channel.
        """
        await deals_service.check_deals(bot=self.bot)
        logging.info("Videos games deals checked whis IsThereAnyDeals API.")

    @tasks.loop(
        time=time(
            hour=fun_config.Quote.QUOTE_FEST_RESET_HOUR,
            minute=fun_config.Quote.QUOTE_FEST_RESET_MINUTE,
            tzinfo=timezone.utc,
        )
    )
    async def fest_end_task(self) -> None:
        """The loop is set at 1st of each month at 18:00.

        Resets the quote channel and announce the winners of this month.
        """
        await quote_fest_service.announce_fest_winners(bot=self.bot)
        logging.info("Monthly quote fest ended.")

    @tasks.loop(hours=1)
    async def swap_activity_task(self) -> None:
        """Task loop every hour.

        Rotates the bot's Discord activity status.
        """
        await activity_service.set_bot_activity(bot=self.bot)
        logging.info("Bot activity swapped.")

    @check_deals_task.before_loop
    @fest_end_task.before_loop
    @swap_activity_task.before_loop
    async def before_task(self) -> None:
        """Wait until the bot is connected for start tasks."""
        await self.bot.wait_until_ready()
