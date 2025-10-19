"""
bot/cogs/reddit.py
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
from bot.core.config_loader import COMMANDS, REGEX
from bot.services.reddit.reddit_service import send_response_with_post_data
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
            logging.info(
                "-- %s said: %s matched with 'reddit url' pattern",
                message.author,
                message.content
            )
            url = regex_search(pattern, message.content)
            await send_response_with_post_data(ctx=message, url=url)

        await self.bot.process_commands(message)

    # pylint: disable=line-too-long
    #  ██████╗ ██████╗ ███╗   ███╗███╗   ███╗ █████╗ ███╗   ██╗██████╗ ███████╗    ██╗      ██████╗  ██████╗ ██╗ ██████╗
    # ██╔════╝██╔═══██╗████╗ ████║████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝    ██║     ██╔═══██╗██╔════╝ ██║██╔════╝
    # ██║     ██║   ██║██╔████╔██║██╔████╔██║███████║██╔██╗ ██║██║  ██║███████╗    ██║     ██║   ██║██║  ███╗██║██║
    # ██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║  ██║╚════██║    ██║     ██║   ██║██║   ██║██║██║
    # ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║██████╔╝███████║    ███████╗╚██████╔╝╚██████╔╝██║╚██████╗
    #  ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝    ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝ ╚═════╝
    # pylint: enable=line-too-long

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
        logging.info(
            "-- %s use /waf slash command with %s url",
            interaction.user.name,
            url
        )
        await send_response_with_post_data(ctx=interaction, url=url)


async def setup(bot):
    """Adds this cog to the given bot"""
    await bot.add_cog(RedditCog(bot))
