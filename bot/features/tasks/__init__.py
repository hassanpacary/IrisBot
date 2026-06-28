"""Background tasks package.

Registers and start all background tasks.
Contains activity tasks, ending quote fest task and deals notification task.

© by hassanpacary
"""

# --- Forward references ---
from __future__ import annotations

# --- Standard library ---
import logging
from typing import TYPE_CHECKING

# --- Internal ---
from bot.features.tasks import tasks

if TYPE_CHECKING:
    from bot.core import bot as b


async def start(bot: b.Bot) -> None:
    """Instantiates the TasksScheduler and starts all background tasks.

    Args:
        bot: The Discord bot instance passed to the scheduler.
    """
    scheduler = tasks.TasksScheduler(bot)
    scheduler.start()
    logging.info("Background tasks started successfully.")
