"""
reddit_commands.py
© by hassanpacary

Cog containing reddit commands for the bot.

Commands:
- /waf : retrieve all images in the post
"""

# --- Imports ---
import re

# --- Third party imports ---
import discord
from discord import app_commands
from discord.ext import commands

# --- Bot modules ---
from functions.reddit_functions import fetch_reddit_medias, send_reddit_medias
from functions.functions import load_json

# Load config data from json files
config = load_json("config.json")
string = load_json(f"string_config_{config['config']['langage']}.json")
regex = load_json("regex_config.json")


class RedditCommands(commands.Cog):
    """
    Cog containing reddit commands for the bot.

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

    @app_commands.command(
        name=string['command']['waf']['slash_command'],
        description=string['command']['waf']['description']
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def waf(self, interaction: discord.Interaction, url: str):
        """
        Command to fetch and send media from a Reddit URL.

        Event:
            Triggered when a user executes the /waf command with a URL argument.

        Action:
            - Validates the provided URL against a Reddit URL pattern.
            - If the URL is invalid, sends an ephemeral warning message.
            - Fetches media from the Reddit URL asynchronously.
            - Sends a response message indicating the number of media items found.
            - If media is found, sends the media to the interaction channel.
        """
        reddit_pattern = re.compile(regex['url_reddit']['pattern'])

        # --- URL not match ---
        if not reddit_pattern.match(url):
            await interaction.response.send_message(string['reddit']['wrong_url'], ephemeral=True)
            return

        medias = await fetch_reddit_medias(url=url)
        await interaction.response.send_message(
            string['reddit']['reply_message_with_medias_count'].format(medias_count=len(medias)))

        if medias:
            await send_reddit_medias(
                medias=medias,
                interaction=interaction
            )

        # This function processes the commands that have been registered to the bot.
        # Without this coroutine, none of the commands will be triggered.
        await self.bot.process_commands(interaction.message)


async def setup(bot):
    """
    Adds this cog to the given bot.

    Args:
        bot (commands.Bot): The bot instance to which the cog will be added.
    """
    await bot.add_cog(RedditCommands(bot))
