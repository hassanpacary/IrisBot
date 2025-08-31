"""
fun_commands.py
© by hassanpacary

Cog containing fun slash commands for the bot.

Commands:
- /quoi : replies with a predefined message (FEUR)
"""

# --- Third party imports ---
import discord
from discord import app_commands
from discord.ext import commands

# --- Bot modules ---
from functions.functions import load_json

# Load config data from json files
config = load_json("config.json")
string = load_json(f"string_config_{config['config']['langage']}.json")


class FunCommands(commands.Cog):
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

    @app_commands.command(
        name=string['command']['quoi']['slash_command'],
        description=string['command']['quoi']['description']
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def quoi(self, interaction: discord.Interaction):
        """
        Responds to the /quoi slash command.

        Args:
            interaction (discord.Interaction): The interaction object triggered by the user.

        Action:
            Sends the message stored in the QUOI variable to the user.
        """
        await interaction.response.send_message(
            string['fun']['reply_feur']
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
    await bot.add_cog(FunCommands(bot))
