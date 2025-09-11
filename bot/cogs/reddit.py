"""
reddit.py
© by hassanpacary

Cog containing reddit commands for the bot.
"""

# --- Imports ---
import logging

# --- Third party imports ---
import discord
from discord import app_commands
from discord.ext import commands

# --- Bot modules ---
from bot.core.config_loader import COMMANDS, STRINGS, REGEX
from bot.services.response_service import send_response_to_discord, reply_with_medias
from bot.utils.strings_utils import matches_pattern, regex_search

# ██████╗ ███████╗██████╗ ██████╗ ██╗████████╗    ██╗    ██╗ ██████╗ ██╗   ██╗███████╗
# ██╔══██╗██╔════╝██╔══██╗██╔══██╗██║╚══██╔══╝    ██║    ██║██╔═══██╗██║   ██║██╔════╝
# ██████╔╝█████╗  ██║  ██║██║  ██║██║   ██║       ██║ █╗ ██║██║   ██║██║   ██║█████╗
# ██╔══██╗██╔══╝  ██║  ██║██║  ██║██║   ██║       ██║███╗██║██║   ██║██║   ██║██╔══╝
# ██║  ██║███████╗██████╔╝██████╔╝██║   ██║       ╚███╔███╔╝╚██████╔╝╚██████╔╝██║
# ╚═╝  ╚═╝╚══════╝╚═════╝ ╚═════╝ ╚═╝   ╚═╝        ╚══╝╚══╝  ╚═════╝  ╚═════╝ ╚═╝


class RedditCog(commands.Cog):
    """Cog containing reddit commands for the bot."""

    def __init__(self, bot):
        """Initialize the cog with a reference to the bot."""
        self.bot = bot

    # ███████╗██╗   ██╗███████╗███╗   ██╗████████╗███████╗    ██╗      ██████╗  ██████╗ ██╗ ██████╗
    # ██╔════╝██║   ██║██╔════╝████╗  ██║╚══██╔══╝██╔════╝    ██║     ██╔═══██╗██╔════╝ ██║██╔════╝
    # █████╗  ██║   ██║█████╗  ██╔██╗ ██║   ██║   ███████╗    ██║     ██║   ██║██║  ███╗██║██║
    # ██╔══╝  ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║   ██║   ╚════██║    ██║     ██║   ██║██║   ██║██║██║
    # ███████╗ ╚████╔╝ ███████╗██║ ╚████║   ██║   ███████║    ███████╗╚██████╔╝╚██████╔╝██║╚██████╗
    # ╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝    ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝ ╚═════╝

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        Event listener that triggers whenever a message is sent in a channel or DM.

        Action:
            - Ignores any message sent by the bot itself.
            - Checks if the message contains a Reddit URL:
                - If found, extracts the URL and calls `reply_reddit` to handle it.
            - Other messages are ignored by this listener.
        """

        # --- Ignore bot message ---
        if message.author == self.bot.user:
            return

        # --- Message that contains Reddit url listener ---
        pattern = REGEX['reddit']['pattern']
        if matches_pattern(pattern, message.content):
            await reply_with_medias(target=message, url=regex_search(pattern, message.content))
            logging.info(f"-- {message.author} said: {message.content} matched with 'reddit url' pattern")

        await self.bot.process_commands(message)

    #  ██████╗ ██████╗ ███╗   ███╗███╗   ███╗ █████╗ ███╗   ██╗██████╗ ███████╗    ██╗      ██████╗  ██████╗ ██╗ ██████╗
    # ██╔════╝██╔═══██╗████╗ ████║████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝    ██║     ██╔═══██╗██╔════╝ ██║██╔════╝
    # ██║     ██║   ██║██╔████╔██║██╔████╔██║███████║██╔██╗ ██║██║  ██║███████╗    ██║     ██║   ██║██║  ███╗██║██║
    # ██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║  ██║╚════██║    ██║     ██║   ██║██║   ██║██║██║
    # ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║██████╔╝███████║    ███████╗╚██████╔╝╚██████╔╝██║╚██████╗
    #  ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝    ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝ ╚═════╝

    @app_commands.command(
        name=COMMANDS['reddit']['waf']['slash_command'],
        description=COMMANDS['reddit']['waf']['description']
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def waf_logic(self, interaction: discord.Interaction, url: str):
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
        if not url:
            return

        responses_strings = STRINGS['reddit']

        # --- URL not match ---
        pattern = REGEX['reddit']['pattern']
        if not matches_pattern(pattern, url):
            await send_response_to_discord(target=interaction, content=responses_strings['wrong_url'], ephemeral=True)
            return

        await reply_with_medias(target=interaction, url=regex_search(pattern, url))
        logging.info(f"-- {interaction.user.name} use /waf slash command with {url} url")


async def setup(bot):
    """
    Adds this cog to the given bot.

    Args:
        bot (commands.Bot): The bot instance to which the cog will be added.
    """
    await bot.add_cog(RedditCog(bot))
