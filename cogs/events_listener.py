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
import os
import re
import logging
import random

# --- Third party imports
import discord
from discord.ext import commands, tasks

# --- bot modules ---
from functions.bot_status_functions import fetch_random_anime, state_constructor
from functions.fun_functions import reply_feur
from functions.functions import load_json
from functions.reddit_functions import reply_reddit
from functions.vocal_functions import text_to_speech

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

        # selects an activity from among the predefined ones
        # or randomly anime from the anilist API
        random_swap = random.randint(0,1)
        if random_swap == 0:
            activity = await fetch_random_anime()
            activity_name = activity['title']['romaji']
            activity_state = await state_constructor(activity)

            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name=activity_name,
                    state=activity_state
                )
            )
        else:
            activity_type, activity_list = random.choice(
                list(string['event']['status_activity']['preset_activity'].items())
            )
            activity = random.choice(list(activity_list.values()))
            activity_name = activity['activity_name']
            activity_state = activity['activity_state']

            if activity_type == 'game':
                await self.bot.change_presence(
                    activity=discord.Game(
                        name=activity_name,
                        state=activity_state
                    )
                )
            if activity_type == 'watching':
                await self.bot.change_presence(
                    activity=discord.Activity(
                        type=discord.ActivityType.watching,
                        name=activity_name,
                        state=activity_state
                    )
                )

        logging.info(
            '%s -- INFO: Bot status set as %s',
            datetime.datetime.now().strftime('%d.%m.%Y %T'), activity_name
        )

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Event triggered when the bot is ready and connected to Discord.

        Action:
            - Prints a log message with the bot's name.
            - swap status message of the bot.
        """
        logging.info(
            '%s -- INFO: Bot connected as %s',
            datetime.datetime.now().strftime('%d.%m.%Y %T'), self.bot.user.name
        )

        print('|--------------------------------------|')
        print('|          The bot is ready !          |')
        print('|--------------------------------------|')

        self.status_swap.start()

        # Sync slash commands in the commands tree
        await self.bot.tree.sync()

    @commands.Cog.listener()
    async def on_resumed(self):
        """
        Event listener triggered when the bot successfully reconnects to Discord.

        Logs the bot's resumption with a timestamp and prints a message to the console.

        Actions:
            - Logs an info message with the bot's username and current timestamp.
            - Prints a message to the console indicating that the bot has resumed.
        """
        logging.info(
            '%s -- INFO: Bot is resumed as %s',
            datetime.datetime.now().strftime('%d.%m.%Y %T'), self.bot.user.name
        )

        print(f'-- The bot is resumed as {self.bot.user.name}')

    @commands.Cog.listener()
    async def on_disconnect(self):
        """
        Event listener triggered when the bot disconnects from Discord.

        This function logs a formatted error message with a timestamp
        whenever the bot loses connection to Discord.

        Actions:
            - Creates an inner async function `error(e: str)` to handle
              logging of the disconnect event.
            - Logs a timestamped message indicating the bot has disconnected.
        """
        # Save a logfile with the error
        async def error(e: str):
            logging.info(
                '%s -- Error: Disconnected !\n%s',
                datetime.datetime.now().strftime('%d.%m.%Y %T'), e
            )

        await error('\n' +
                    '|---------------------------------------------|' + '\n' +
                    '|          The bot is disconnected !          |' + '\n' +
                    '|---------------------------------------------|')

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """
        Event triggered when a new member joins the server.

        Args:
            member (discord.Member): The member who joined the server.

        Action:
            Sends a welcome message in the server's system channel.
        """

        if member.guild.system_channel is not None:
            await member.guild.system_channel.send(
                random.choice(string['event']['welcome_new_user']).format(member=member.mention)
            )
        else:
            await member.guild.fetch_channel(string['event']['welcome_channel_id']).send(
                random.choice(string['event']['welcome_new_user']).format(member=member.mention)
            )

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
            await reply_reddit(message=message, url=reddit_pattern.match(message.content).group(0))

        # --- Message that contains 'quoi' listener ---
        elif quoi_word_pattern.match(message.content):
            await reply_feur(message=message)

        # --- Text to speech event listener ---
        elif (
                message_author_voice_state
                and bot_voice_client
                and message_author_voice_state.channel == bot_voice_client.channel
                and message.channel.id == config['channels']['textuel_vocal_channel']
        ):

            if not os.getenv('AZURE_KEY') or not os.getenv('AZURE_ENDPOINT'):
                logging.warning(
                    '%s -- Warning: Unable to load AZURE environment variables.',
                    datetime.datetime.now().strftime('%d.%m.%Y %T')
                )
            await text_to_speech(self, message=message)

        # This function processes the commands that have been registered to the bot
        # and other groups.
        # Without this coroutine, none of the commands will be triggered.
        await self.bot.process_commands(message)


async def setup(bot):
    """
    Adds this cog to the given bot.

    Args:
        bot (commands.Bot): The bot instance to which the cog will be added.
    """
    await bot.add_cog(Events(bot))
