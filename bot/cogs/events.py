"""
events.py
© by hassanpacary

Cog containing events listener of the bot.
"""

# --- Imports ---
import logging
import random

# --- Third party imports ---
import discord
from discord.ext import commands, tasks

# --- bot modules ---
from bot.services.activity_service import set_bot_activity, random_activity


#  ██████╗ ██╗      ██████╗ ██████╗  █████╗ ██╗         ███████╗██╗   ██╗███████╗███╗   ██╗████████╗███████╗
# ██╔════╝ ██║     ██╔═══██╗██╔══██╗██╔══██╗██║         ██╔════╝██║   ██║██╔════╝████╗  ██║╚══██╔══╝██╔════╝
# ██║  ███╗██║     ██║   ██║██████╔╝███████║██║         █████╗  ██║   ██║█████╗  ██╔██╗ ██║   ██║   ███████╗
# ██║   ██║██║     ██║   ██║██╔══██╗██╔══██║██║         ██╔══╝  ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║   ██║   ╚════██║
# ╚██████╔╝███████╗╚██████╔╝██████╔╝██║  ██║███████╗    ███████╗ ╚████╔╝ ███████╗██║ ╚████║   ██║   ███████║
#  ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝    ╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝


class EventsCog(commands.Cog):
    """Cog containing events listener of the bot."""

    def __init__(self, bot):
        """Initialize the cog with a reference to the bot."""
        self.bot = bot

    # ██████╗  ██████╗ ████████╗    ███████╗████████╗ █████╗ ████████╗███████╗
    # ██╔══██╗██╔═══██╗╚══██╔══╝    ██╔════╝╚══██╔══╝██╔══██╗╚══██╔══╝██╔════╝
    # ██████╔╝██║   ██║   ██║       ███████╗   ██║   ███████║   ██║   █████╗
    # ██╔══██╗██║   ██║   ██║       ╚════██║   ██║   ██╔══██║   ██║   ██╔══╝
    # ██████╔╝╚██████╔╝   ██║       ███████║   ██║   ██║  ██║   ██║   ███████╗
    # ╚═════╝  ╚═════╝    ╚═╝       ╚══════╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝   ╚══════╝

    @tasks.loop(hours=1)
    async def status_swap(self):
        """Background task that updates the bot's presence every hour."""

        # --- Get random activity ---
        activity_name, activity_type, activity_state = await random_activity()

        # --- Set bot activity ---
        await set_bot_activity(
            bot=self.bot,
            activity_name=activity_name,
            activity_type=activity_type,
            activity_state=activity_state
        )

    @commands.Cog.listener()
    async def on_ready(self):
        """Event triggered when the bot is ready and connected to Discord."""
        on_ready_banner = r"""
        ██╗      ██████╗  █████╗ ██████╗ ██╗███╗   ██╗ ██████╗      ██╗ ██████╗  ██████╗ ██╗ ██╗
        ██║     ██╔═══██╗██╔══██╗██╔══██╗██║████╗  ██║██╔════╝     ███║██╔═████╗██╔═████╗╚═╝██╔╝
        ██║     ██║   ██║███████║██║  ██║██║██╔██╗ ██║██║  ███╗    ╚██║██║██╔██║██║██╔██║  ██╔╝ 
        ██║     ██║   ██║██╔══██║██║  ██║██║██║╚██╗██║██║   ██║     ██║████╔╝██║████╔╝██║ ██╔╝  
        ███████╗╚██████╔╝██║  ██║██████╔╝██║██║ ╚████║╚██████╔╝     ██║╚██████╔╝╚██████╔╝██╔╝██╗
        ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝      ╚═╝ ╚═════╝  ╚═════╝ ╚═╝ ╚═╝                                                        
        """

        logging.info(on_ready_banner)
        logging.info(f"-- Bot connected as {self.bot.user.name}")

        # Starts the background task that changes the bot's activity
        self.status_swap.start()

    @commands.Cog.listener()
    async def on_resumed(self):
        """Event listener triggered when the bot successfully reconnects."""
        logging.info(f"-- Bot is resumed as {self.bot.user.name}")

    # ███╗   ██╗███████╗██╗    ██╗    ███╗   ███╗███████╗███╗   ███╗██████╗ ███████╗██████╗
    # ████╗  ██║██╔════╝██║    ██║    ████╗ ████║██╔════╝████╗ ████║██╔══██╗██╔════╝██╔══██╗
    # ██╔██╗ ██║█████╗  ██║ █╗ ██║    ██╔████╔██║█████╗  ██╔████╔██║██████╔╝█████╗  ██████╔╝
    # ██║╚██╗██║██╔══╝  ██║███╗██║    ██║╚██╔╝██║██╔══╝  ██║╚██╔╝██║██╔══██╗██╔══╝  ██╔══██╗
    # ██║ ╚████║███████╗╚███╔███╔╝    ██║ ╚═╝ ██║███████╗██║ ╚═╝ ██║██████╔╝███████╗██║  ██║
    # ╚═╝  ╚═══╝╚══════╝ ╚══╝╚══╝     ╚═╝     ╚═╝╚══════╝╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """
        Event triggered when a new member joins the server.

        Action:
            Sends a welcome message in the server's system channel.
        """
        system_channel_id = member.guild.system_channel.id
        welcome_channel_id = self.bot.config['bot']['channels']['welcome_channel_id']
        welcome_message = random.choice(self.bot.config['strings']['event']['welcome_new_user']).format(
            member=member.mention)

        # If a welcome channel has been set up, we use this one
        if member.guild.fetch_channel(welcome_channel_id):
            system_channel_id = welcome_channel_id

        channel = await member.guild.fetch_channel(system_channel_id)
        await channel.send(welcome_message)


async def setup(bot):
    """Adds this cog to the given bot."""
    await bot.add_cog(EventsCog(bot))
