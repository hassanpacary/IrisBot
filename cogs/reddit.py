"""
reddit.py

Cog containing sauce commands and events for the bot.

Commands:
- waf : retrieve all images in the post

Events:
- on_message : if message contains reddit URL, retrieve all images in the post
"""


import discord
from discord import app_commands
from discord.ext import commands
from config.regex import REDDIT_URL_REGEX
from config.string_fr import REDDIT_RESPONSE_MESSAGE, REDDIT_WRONG_URL
from utils.reddit_utils import fetch_reddit_images, send_reddit_images


class SauceForReddit(commands.Cog):
    """
    Cog containing sauce commands and events for the bot.

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


    @app_commands.command(name="waf", description="Toutes tes vilaines images.")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def waf(self, interaction: discord.Interaction, url: str):
        """
        Slash command that retrieves and sends all images from a Reddit post.

        Workflow:
            1. Validates that the provided URL is a valid Reddit link.
               - If not valid, sends an ephemeral error message to the user.
            2. Sends a confirmation response message.
            3. Fetches all images from the Reddit submission.
            4. Sends the images in batches to the same channel.

        Args:
            interaction (discord.Interaction): The Discord interaction that triggered the command.
            url (str): The Reddit post URL provided by the user.
        """
        if not REDDIT_URL_REGEX.match(url):
            await interaction.response.send_message(REDDIT_WRONG_URL, ephemeral=True)
            return
        images = await fetch_reddit_images(url=url)

        await interaction.response.send_message(REDDIT_RESPONSE_MESSAGE.format(image_count=len(images)))

        if images:
            await send_reddit_images(images=images, interaction=interaction)


async def setup(bot):
    """
    Adds this cog to the given bot.

    Args:
        bot (commands.Bot): The bot instance to which the cog will be added.
    """
    await bot.add_cog(SauceForReddit(bot))