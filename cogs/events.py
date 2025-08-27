"""
events.py

Cog containing events listener of the bot.

Events:
- on_ready : Event triggered when the bot is ready and connected to Discord.
- on_member_join : Event triggered when a new member joins the server.
- on_message : Event triggered when a message is sent.
"""


import discord
import random
from discord.ext import commands, tasks
from config.regex import FUN_QUOIFEUR_REGEX, REDDIT_URL_REGEX
from config.string_fr import ON_READY, WELCOME, STATUS
from utils.fun_utils import reply_feur
from utils.reddit_utils import reply_reddit
from utils.vocal_utils import text_to_speech


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

        # Sync slash commands in the commands tree
        await self.bot.tree.sync()


    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """
        Event triggered when a new member joins the server.

        Args:
            member (discord.Member): The member who joined the server.

        Action:
            Sends a welcome message in the server's system channel.
        """
        welcome_channel = member.guild.system_channel
        await welcome_channel.send(random.choice(WELCOME).format(member=member.mention))


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        Event listener that triggers whenever a message is sent in a channel or DM.

        Workflow:
            1. Ignores any message sent by the bot itself.
            2. Checks if the message contains a Reddit URL:
                - If found, extracts the URL and calls `reply_reddit` to handle it.
            3. Checks if the message matches the "quoi-feur" pattern:
                - If matched, calls `reply_feur` to reply with the predefined response.
            4. Check if the message is send in the vocal channel and if Iris is in vocal
                - If matched, calls text_to_speech for TTS
            5. Other messages are ignored by this listener.

        Args:
            message (discord.Message): The message sent by a user.
        """
        if message.author == self.bot.user:
            return

        message_author_channel = message.author.voice.channel
        bot_voice_client = discord.utils.get(self.bot.voice_clients, guild=message.guild)

        # Reddit regex URL listener
        if REDDIT_URL_REGEX.match(message.content):
            url = REDDIT_URL_REGEX.match(message.content).group(0)
            await reply_reddit(self, message=message, url=url)

        # Quoi - feur listener
        elif FUN_QUOIFEUR_REGEX.match(message.content):
            await reply_feur(message=message)

        # Text to speech event listener
        elif message.author.voice and bot_voice_client and message_author_channel == bot_voice_client.channel and message.channel.id == 594583967554994178:
            await text_to_speech(self, message=message)


async def setup(bot):
    """
    Adds this cog to the given bot.

    Args:
        bot (commands.Bot): The bot instance to which the cog will be added.
    """
    await bot.add_cog(Events(bot))