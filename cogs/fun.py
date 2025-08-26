"""
fun.py

Cog containing fun slash commands for the bot.

Commands:
- /quoi : replies with a predefined message (FEUR)
"""


import discord
from discord import app_commands
from discord.ext import commands
from config.string_fr import FEUR


class Fun(commands.Cog):
    """
    Cog containing fun commands for the bot.

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


    @app_commands.command(name="quoi", description="répond 'feur'.")
    async def quoi(self, interaction: discord.Interaction):
        """
        Responds to the /quoi slash command.

        Args:
            interaction (discord.Interaction): The interaction object triggered by the user.

        Action:
            Sends the message stored in the QUOI variable to the user.
        """
        await interaction.response.send_message(FEUR)


async def setup(bot):
    """
    Adds this cog to the given bot.

    Args:
        bot (commands.Bot): The bot instance to which the cog will be added.
    """
    await bot.add_cog(Fun(bot))