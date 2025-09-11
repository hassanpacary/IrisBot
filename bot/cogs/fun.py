"""
fun.py
© by hassanpacary

Cog containing fun slash commands logic.
"""

# --- Imports ---
import logging
import random

# --- Third party imports ---
import discord
from discord import app_commands
from discord.ext import commands

# --- Bot modules ---
from bot.core.config_loader import COMMANDS, STRINGS, REGEX
from bot.services.response_service import send_response_to_discord
from bot.utils.strings_utils import matches_pattern

#  ██████╗██╗   ██╗███╗   ██╗███╗   ██╗██╗   ██╗
# ██╔════╝██║   ██║████╗  ██║████╗  ██║╚██╗ ██╔╝
# ██║     ██║   ██║██╔██╗ ██║██╔██╗ ██║ ╚████╔╝
# ██║     ██║   ██║██║╚██╗██║██║╚██╗██║  ╚██╔╝
# ╚██████╗╚██████╔╝██║ ╚████║██║ ╚████║   ██║
#  ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝   ╚═╝


class FunCog(commands.Cog):
    """Cog containing fun commands for the bot."""

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
            - Checks if the message matches the "quoi-feur" pattern:
                - If matched, calls `reply_feur` to reply with the predefined response.
            - Other messages are ignored by this listener.
        """

        # --- Ignore bot message ---
        if message.author == self.bot.user:
            return

        # --- Message that contains 'quoi' listener ---
        pattern = REGEX['quoi']['pattern']

        if matches_pattern(pattern, message.content):
            await send_response_to_discord(target=message, content=STRINGS['fun']['quoi'])
            logging.info(f"-- {message.author} said: {message.content} and matched with 'quoi' pattern")

        await self.bot.process_commands(message)

    #  ██████╗ ██████╗ ███╗   ███╗███╗   ███╗ █████╗ ███╗   ██╗██████╗ ███████╗    ██╗      ██████╗  ██████╗ ██╗ ██████╗
    # ██╔════╝██╔═══██╗████╗ ████║████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝    ██║     ██╔═══██╗██╔════╝ ██║██╔════╝
    # ██║     ██║   ██║██╔████╔██║██╔████╔██║███████║██╔██╗ ██║██║  ██║███████╗    ██║     ██║   ██║██║  ███╗██║██║
    # ██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║  ██║╚════██║    ██║     ██║   ██║██║   ██║██║██║
    # ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║██████╔╝███████║    ███████╗╚██████╔╝╚██████╔╝██║╚██████╗
    #  ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝    ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝ ╚═════╝

    @app_commands.command(
        name=COMMANDS['fun']['quoi']['slash_command'],
        description=COMMANDS['fun']['quoi']['description']
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def quoi_logic(self, interaction: discord.Interaction):
        """
        Responds to the /quoi slash command.

        Args:
            interaction (discord.Interaction): The interaction object triggered by the user.

        Action:
            Sends the message stored in the QUOI variable to the user.
        """
        await send_response_to_discord(target=interaction, content=STRINGS['fun']['quoi'])
        logging.info(f"-- {interaction.user.name} use /quoi slash command")

    @app_commands.command(
        name=COMMANDS['fun']['roll']['slash_command'],
        description=COMMANDS['fun']['roll']['description']
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def roll_logic(self, interaction: discord.Interaction, sides: int = 6):
        """
        Responds to the /roll slash command.

        Args:
            interaction (discord.Interaction): The interaction object triggered by the user.
            sides (int): The number of sides to roll. Default is 6.

        Action:
            Sends a random number between 1 and the number of sides.
        """
        random_number_1 = random.randint(1, sides)
        random_number_2 = random_number_1

        while random_number_1 == random_number_2:
            random_number_2 = random.randint(1, sides)

        await send_response_to_discord(
            target=interaction,
            content=STRINGS['fun']['roll_result'].format(
                first_result = random_number_1,
                second_result = random_number_2
            )
        )
        logging.info(f"-- {interaction.user.name} use /roll slash command for dice with {sides} sides. Result: {random_number_1}, {random_number_2}")


async def setup(bot):
    """Adds this cog to the given bot."""
    await bot.add_cog(FunCog(bot))
