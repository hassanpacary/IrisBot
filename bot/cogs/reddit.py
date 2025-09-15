"""
reddit.py
© by hassanpacary

Cog containing reddit commands and their logic.
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
    """Reddit cog class"""

    def __init__(self, bot):
        """Initialize the cog with a reference to the bot"""
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
        Event listener that triggers whenever a message is sent in a channel

        Parameters:
            message (discord.Message): The message who trigger the listener

        Actions:
            - Checks if the message contains a Reddit URL
            - If found, extracts the URL and calls `reply_with_medias`

        this event responds to the url of a reddit post.
        This response contains an embed with all the post's information,
        followed by the post's various medias
        """

        # --- Ignore bot message ---
        if message.author == self.bot.user:
            return

        pattern = REGEX['reddit']['pattern']

        if matches_pattern(pattern, message.content):
            logging.info(f"-- {message.author} said: {message.content} matched with 'reddit url' pattern")
            await reply_with_medias(target=message, url=regex_search(pattern, message.content))

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
        Responds to the /waf slash command

        Parameters:
            interaction (discord.Interaction): The interaction object triggered by the user
            url (str): The url of the Reddit post

        Action:
            - Checks if Reddit URL matches with the regex pattern
            - If the URL is invalid, sends an ephemeral warning message
            - If matches, calls `reply_with_medias` with the url

        The response of command contains an embed with all the post's information,
        followed by the post's various medias
        """
        logging.info(f"-- {interaction.user.name} use /waf slash command with {url} url")

        responses_strings = STRINGS['reddit']
        pattern = REGEX['reddit']['pattern']

        if not matches_pattern(pattern, url):
            await send_response_to_discord(target=interaction, content=responses_strings['wrong_url'], ephemeral=True)
            return

        await reply_with_medias(target=interaction, url=regex_search(pattern, url))


async def setup(bot):
    """Adds this cog to the given bot"""
    await bot.add_cog(RedditCog(bot))
