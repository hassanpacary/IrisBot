"""
events_listener.py
© by hassanpacary

Cog containing events listener of the bot.

Events:
- on_ready : Event triggered when the bot is ready and connected to Discord.*
- on_resumed : Event triggered when the bot is connected to Discord.
- on_disconnected : Event triggered when the bot is disconnected.
- on_member_join : Event triggered when a new member joins the server.
- on_message : Event triggered when a message is sent.
"""

# --- Imports ---
import datetime
import re

import discord
import logging
import random
from discord.ext import commands, tasks

# --- bot modules ---
from functions.fun_functions import reply_feur
from functions.reddit_functions import reply_reddit
from functions.vocal_functions import text_to_speech
from functions.functions import load_json

# Load config data from json files
config = load_json("config.json")
string = load_json(f"string_config_{config['config']['langage']}.json")
regex = load_json("regex_config.json")

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
        activity_type, activity = random.choice(list(string['event']['status_activity_list'].items()))
        if activity_type == 'game':
            await self.bot.change_presence(activity=discord.Game(random.choice(activity)))
        if activity_type == 'watching':
            await self.bot.change_presence(
                activity=discord.Activity(type=discord.ActivityType.watching, name=random.choice(activity)))

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Event triggered when the bot is ready and connected to Discord.

        Action:
            - Prints a log message with the bot's name.
            - swap status message of the bot.
        """
        logging.info(string['log']['on_ready'].format(bot_name=self.bot.user.name))
        print(string['log']['on_ready'].format(bot_name=self.bot.user.name))
        self.status_swap.start()

        # Sync slash commands in the commands tree
        await self.bot.tree.sync()

    @commands.Cog.listener()
    async def on_resumed(self):
        logging.info(string['log']['on_resumed'].format(bot_name=self.bot.user.name))

    @commands.Cog.listener()
    async def on_disconnect(self):

        # Save a logfile with the error
        async def error(text: str):
            logging.info(str(datetime.datetime.now().strftime('%d.%m.%Y %T')) + ' -- Error: ' + str(text))

        await error(string['log']['on_disconnected'].format(bot_name=self.bot.user.name))

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """
        Event triggered when a new member joins the server.

        Args:
            member (discord.Member): The member who joined the server.

        Action:
            Sends a welcome message in the server's system channel.
        """
        await member.guild.system_channel.send(random.choice(string['event']['welcome_new_user']).format(member=member.mention))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        Event listener that triggers whenever a message is sent in a channel or DM.

        Args:
            message (discord.Message): The message sent by a user.

        Action:
            1. Ignores any message sent by the bot itself.
            2. Checks if the message contains a Reddit URL:
                - If found, extracts the URL and calls `reply_reddit` to handle it.
            3. Checks if the message matches the "quoi-feur" pattern:
                - If matched, calls `reply_feur` to reply with the predefined response.
            4. Check if the message is sent in the vocal channel (textuel) and if Iris is in vocal
                - If matched, calls text_to_speech for TTS
            5. Other messages are ignored by this listener.
        """

        # --- Ignore bot message ---
        if message.author == self.bot.user:
            return

        message_author_voice_state = message.author.voice
        bot_voice_client = discord.utils.get(self.bot.voice_clients, guild=message.guild)

        reddit_pattern = re.compile(regex['url_reddit']['pattern'])
        quoi_word_pattern = re.compile(regex['quoi_word']['pattern'], flags=re.IGNORECASE)

        # --- Reddit regex URL listener ---
        if reddit_pattern.match(message.content):
            await reply_reddit(self, message=message, url=reddit_pattern.match(message.content).group(0))

        # --- Message that contains 'quoi' listener ---
        elif quoi_word_pattern.match(message.content):
            await reply_feur(message=message)

        # --- Text to speech event listener ---
        elif (message_author_voice_state
              and bot_voice_client
              and message_author_voice_state.channel == bot_voice_client.channel
              and message.channel.id == config['channels']['welcome_channel_id']):
            await text_to_speech(self, message=message)


async def setup(bot):
    """
    Adds this cog to the given bot.

    Args:
        bot (commands.Bot): The bot instance to which the cog will be added.
    """
    await bot.add_cog(Events(bot))
