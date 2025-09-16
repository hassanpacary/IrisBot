"""
bot/cogs/events.py
© by hassanpacary

Cog containing globals events listener and their logic
"""

# --- Imports ---
import logging
import random

# --- Third party imports ---
import discord
from discord.ext import commands

# --- bot modules ---
from bot.core.config_loader import BOT, STRINGS, ON_READY_BANNER


#  ██████╗ ██╗      ██████╗ ██████╗  █████╗ ██╗         ███████╗██╗   ██╗███████╗███╗   ██╗████████╗███████╗
# ██╔════╝ ██║     ██╔═══██╗██╔══██╗██╔══██╗██║         ██╔════╝██║   ██║██╔════╝████╗  ██║╚══██╔══╝██╔════╝
# ██║  ███╗██║     ██║   ██║██████╔╝███████║██║         █████╗  ██║   ██║█████╗  ██╔██╗ ██║   ██║   ███████╗
# ██║   ██║██║     ██║   ██║██╔══██╗██╔══██║██║         ██╔══╝  ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║   ██║   ╚════██║
# ╚██████╔╝███████╗╚██████╔╝██████╔╝██║  ██║███████╗    ███████╗ ╚████╔╝ ███████╗██║ ╚████║   ██║   ███████║
#  ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝    ╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝


class EventsCog(commands.Cog):
    """Event cog class"""

    def __init__(self, bot):
        """Initialize the cog with a reference to the bot"""
        self.bot = bot

    # ██████╗  ██████╗ ████████╗    ███████╗████████╗ █████╗ ████████╗███████╗
    # ██╔══██╗██╔═══██╗╚══██╔══╝    ██╔════╝╚══██╔══╝██╔══██╗╚══██╔══╝██╔════╝
    # ██████╔╝██║   ██║   ██║       ███████╗   ██║   ███████║   ██║   █████╗
    # ██╔══██╗██║   ██║   ██║       ╚════██║   ██║   ██╔══██║   ██║   ██╔══╝
    # ██████╔╝╚██████╔╝   ██║       ███████║   ██║   ██║  ██║   ██║   ███████╗
    # ╚═════╝  ╚═════╝    ╚═╝       ╚══════╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝   ╚══════╝

    @commands.Cog.listener()
    async def on_ready(self):
        """Event triggered when the bot is ready and connected to Discord"""
        logging.info(ON_READY_BANNER)
        logging.info(f"-- Bot connected as {self.bot.user.name}")

    @commands.Cog.listener()
    async def on_resumed(self):
        """Event listener triggered when the bot successfully reconnects"""
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
        Event triggered when a new member joins the server

        Parameters:
            member (discord.Member): The member who joined the server

        Action:
            Sends a welcome message in the server's system channel
        """
        system_channel_id = member.guild.system_channel.id

        welcome_channel_id = BOT['channels']['welcome_channel_id']
        welcome_message = random.choice(STRINGS['event']['welcome_message']).format(
            member=member.mention)

        # If a welcome channel has been set up, we use this one
        if await member.guild.fetch_channel(welcome_channel_id):
            system_channel_id = welcome_channel_id

        channel = await member.guild.fetch_channel(system_channel_id)
        await channel.send(welcome_message)
        logging.info(f"-- New member joined {member.name}")

    # ██████╗ ███████╗███╗   ███╗ ██████╗ ██╗   ██╗███████╗    ███╗   ███╗███████╗███╗   ███╗██████╗ ███████╗██████╗
    # ██╔══██╗██╔════╝████╗ ████║██╔═══██╗██║   ██║██╔════╝    ████╗ ████║██╔════╝████╗ ████║██╔══██╗██╔════╝██╔══██╗
    # ██████╔╝█████╗  ██╔████╔██║██║   ██║██║   ██║█████╗      ██╔████╔██║█████╗  ██╔████╔██║██████╔╝█████╗  ██████╔╝
    # ██╔══██╗██╔══╝  ██║╚██╔╝██║██║   ██║╚██╗ ██╔╝██╔══╝      ██║╚██╔╝██║██╔══╝  ██║╚██╔╝██║██╔══██╗██╔══╝  ██╔══██╗
    # ██║  ██║███████╗██║ ╚═╝ ██║╚██████╔╝ ╚████╔╝ ███████╗    ██║ ╚═╝ ██║███████╗██║ ╚═╝ ██║██████╔╝███████╗██║  ██║
    # ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝ ╚═════╝   ╚═══╝  ╚══════╝    ╚═╝     ╚═╝╚══════╝╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """
        Event triggered when a member leave the server

        Parameters:
            member (discord.Member): The member who left the server

        Action:
            Sends a leave message in the server's system channel
        """
        system_channel_id = member.guild.system_channel.id

        goodbye_channel_id = BOT['channels']['goodbye_channel_id']
        goodbye_message = random.choice(STRINGS['event']['goodbye_message']).format(
            member=member.mention)

        # If a goodbye channel has been set up, we use this one
        if await member.guild.fetch_channel(goodbye_channel_id):
            system_channel_id = goodbye_channel_id

        channel = await member.guild.fetch_channel(system_channel_id)
        await channel.send(goodbye_message)
        logging.info(f"-- member leave server {member.name}")


async def setup(bot):
    """Adds this cog to the given bot"""
    await bot.add_cog(EventsCog(bot))
