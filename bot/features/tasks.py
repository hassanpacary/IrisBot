"""
bot/cogs/scheduler.py
© by hassanpacary

Tasks scheduler and their logic
"""

# --- Imports ---
import logging
from datetime import datetime

# --- Third party imports ---
from discord.ext import tasks

# --- bot modules ---
from bot.services.guild.activity_component import set_bot_activity
from bot.services.fun.quote_component import reset_quote


# ███████╗ ██████╗██╗  ██╗███████╗██████╗ ██╗   ██╗██╗     ███████╗██████╗
# ██╔════╝██╔════╝██║  ██║██╔════╝██╔══██╗██║   ██║██║     ██╔════╝██╔══██╗
# ███████╗██║     ███████║█████╗  ██║  ██║██║   ██║██║     █████╗  ██████╔╝
# ╚════██║██║     ██╔══██║██╔══╝  ██║  ██║██║   ██║██║     ██╔══╝  ██╔══██╗
# ███████║╚██████╗██║  ██║███████╗██████╔╝╚██████╔╝███████╗███████╗██║  ██║
# ╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝


class TasksScheduler:
    """Tasks scheduler class"""

    def __init__(self, bot):
        """Initialize the tasks with a reference to the bot"""
        self.bot = bot

    def start(self):
        """Start all background tasks"""
        self.swap_activity_task.start()
        self.reset_quote_task.start()

    #  █████╗  ██████╗████████╗██╗██╗   ██╗██╗████████╗██╗   ██╗
    # ██╔══██╗██╔════╝╚══██╔══╝██║██║   ██║██║╚══██╔══╝╚██╗ ██╔╝
    # ███████║██║        ██║   ██║██║   ██║██║   ██║    ╚████╔╝
    # ██╔══██║██║        ██║   ██║╚██╗ ██╔╝██║   ██║     ╚██╔╝
    # ██║  ██║╚██████╗   ██║   ██║ ╚████╔╝ ██║   ██║      ██║
    # ╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═══╝  ╚═╝   ╚═╝      ╚═╝

    @tasks.loop(hours=1)
    async def swap_activity_task(self):
        """Background task that updates the bot's presence every hour"""
        await set_bot_activity(ctx=self.bot)
        logging.info("-- Swapped activity")

    #  ██████╗ ██╗   ██╗ ██████╗ ████████╗███████╗
    # ██╔═══██╗██║   ██║██╔═══██╗╚══██╔══╝██╔════╝
    # ██║   ██║██║   ██║██║   ██║   ██║   █████╗
    # ██║▄▄ ██║██║   ██║██║   ██║   ██║   ██╔══╝
    # ╚██████╔╝╚██████╔╝╚██████╔╝   ██║   ███████╗
    #  ╚══▀▀═╝  ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝

    @tasks.loop(hours=1)
    async def reset_quote_task(self):
        """Background task that reset the quote channel every month"""
        now = datetime.now()

        if now.day == 1 and now.hour == 18:
            await reset_quote(ctx=self.bot)
            logging.info("-- Monthly reset of the quote channel")
