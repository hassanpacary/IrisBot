"""
events.py

Cog containing events listener of the bot.

Events:
- on_ready : Event triggered when the bot is ready and connected to Discord.
- on_member_join : vent triggered when a new member joins the server.
"""


import discord
import random
from discord.ext import commands, tasks
from config.string_fr import ON_READY, WELCOME, STATUS


class Events(commands.Cog):
    """
    Cog containing events listener of the bot.

    Attributes:
        bot (commands.Bot): The main bot instance.
    """

    def __init__(self, bot):
        """
        Initialize the cog with a reference to the bot.

        Args:
            bot (commands.Bot): The bot instance.
        """
        self.bot = bot


    @tasks.loop(hours=1)
    async def status_swap(self):
        """
        Background task that updates the bot's presence every hour.

        Action:
            Randomly selects a status message from the STATUS list
            and sets it as the bot's current activity.
        """
        await self.bot.change_presence(activity=discord.Game(random.choice(STATUS)))


    @commands.Cog.listener()
    async def on_ready(self):
        """
        Event triggered when the bot is ready and connected to Discord.

        Action:
            - Prints a log message with the bot's name.
            - swap status message of the bot.
        """
        print(ON_READY.format(bot_name=self.bot.user.name))
        self.status_swap.start()


    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        Event triggered when a new member joins the server.

        Args:
            member (discord.Member): The member who joined the server.

        Action:
            Sends a welcome message in the server's system channel.
        """
        welcome_channel = member.guild.system_channel
        await welcome_channel.send(random.choice(WELCOME).format(member=member.mention))


async def setup(bot):
    """
    Adds this cog to the given bot.

    Args:
        bot (commands.Bot): The bot instance to which the cog will be added.
    """
    await bot.add_cog(Events(bot))