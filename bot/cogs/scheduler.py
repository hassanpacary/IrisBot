"""
bot/cogs/scheduler.py
© by hassanpacary

Cog containing globals scheduler and their logic
"""

# --- Imports ---
import logging
from datetime import datetime

# --- Third party imports ---
from discord.ext import commands, tasks

# --- bot modules ---
from bot.services.activity_service import random_activity, set_bot_activity
from bot.services.quotes_service import reset_quote


# ███████╗ ██████╗██╗  ██╗███████╗██████╗ ██╗   ██╗██╗     ███████╗██████╗
# ██╔════╝██╔════╝██║  ██║██╔════╝██╔══██╗██║   ██║██║     ██╔════╝██╔══██╗
# ███████╗██║     ███████║█████╗  ██║  ██║██║   ██║██║     █████╗  ██████╔╝
# ╚════██║██║     ██╔══██║██╔══╝  ██║  ██║██║   ██║██║     ██╔══╝  ██╔══██╗
# ███████║╚██████╗██║  ██║███████╗██████╔╝╚██████╔╝███████╗███████╗██║  ██║
# ╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝


class SchedulerCog(commands.Cog):
    """Event cog class"""

    def __init__(self, bot):
        """Initialize the cog with a reference to the bot"""
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Event triggered when the bot is ready and connected to Discord"""

        # Start all background task
        self.swap_status_task.start()
        self.reset_quote_task.start()

    #  █████╗  ██████╗████████╗██╗██╗   ██╗██╗████████╗██╗   ██╗
    # ██╔══██╗██╔════╝╚══██╔══╝██║██║   ██║██║╚══██╔══╝╚██╗ ██╔╝
    # ███████║██║        ██║   ██║██║   ██║██║   ██║    ╚████╔╝
    # ██╔══██║██║        ██║   ██║╚██╗ ██╔╝██║   ██║     ╚██╔╝
    # ██║  ██║╚██████╗   ██║   ██║ ╚████╔╝ ██║   ██║      ██║
    # ╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═══╝  ╚═╝   ╚═╝      ╚═╝

    @tasks.loop(hours=1)
    async def swap_status_task(self):
        """Background task that updates the bot's presence every hour"""
        activity_name, activity_type, activity_state = await random_activity()

        await set_bot_activity(
            bot=self.bot,
            activity_name=activity_name,
            activity_type=activity_type,
            activity_state=activity_state
        )

        logging.info(f"-- Swapped activity name: {activity_name}, type: {activity_type}, state: {activity_state}")

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
            await reset_quote(self.bot)


async def setup(bot):
    """Adds this cog to the given bot"""
    await bot.add_cog(SchedulerCog(bot))
