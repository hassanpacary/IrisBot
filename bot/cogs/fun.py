"""
bot/cogs/fun.py
© by hassanpacary

Cog containing fun slash commands and their logic
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
    """Fun cog class"""

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
        Event listener that triggers whenever a message is sent in a channel

        Parameters:
            message (discord.Message): The message who trigger the listener

        Actions:
            - Checks if the message matche with 'quoi' regex pattern
            - If found, reply to the user with 'feur'
        """

        # --- Ignore bot message ---
        if message.author == self.bot.user:
            return

        pattern = REGEX['quoi']['pattern']

        if matches_pattern(pattern, message.content):
            logging.info(f"-- {message.author} said: {message.content} and matched with 'quoi' pattern")
            await send_response_to_discord(target=message, content=STRINGS['fun']['quoi'])

        await self.bot.process_commands(message)

    #  ██████╗ ██████╗ ███╗   ███╗███╗   ███╗ █████╗ ███╗   ██╗██████╗ ███████╗    ██╗      ██████╗  ██████╗ ██╗ ██████╗
    # ██╔════╝██╔═══██╗████╗ ████║████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝    ██║     ██╔═══██╗██╔════╝ ██║██╔════╝
    # ██║     ██║   ██║██╔████╔██║██╔████╔██║███████║██╔██╗ ██║██║  ██║███████╗    ██║     ██║   ██║██║  ███╗██║██║
    # ██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║  ██║╚════██║    ██║     ██║   ██║██║   ██║██║██║
    # ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║██████╔╝███████║    ███████╗╚██████╔╝╚██████╔╝██║╚██████╗
    #  ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝    ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝ ╚═════╝

    @app_commands.command(
        name=COMMANDS['fun']['quoi']['slash_command'],
        description=COMMANDS['fun']['quoi']['description'],
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def quoi_logic(self, interaction: discord.Interaction):
        """
        Responds to the /quoi slash command

        Parameters:
            interaction (discord.Interaction): The interaction object triggered by the user

        Action:
            - Reply to the user with 'feur'
        """
        logging.info(f"-- {interaction.user.name} use /quoi slash command")
        await send_response_to_discord(target=interaction, content=STRINGS['fun']['quoi'])

    @app_commands.command(
        name=COMMANDS['fun']['roll']['slash_command'],
        description=COMMANDS['fun']['roll']['description']
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def roll_logic(self, interaction: discord.Interaction, sides: int = 6):
        """
        Responds to the /roll slash command

        Parameters:
            interaction (discord.Interaction): The interaction object triggered by the user
            sides (int): The number of sides to roll. (Default 6)

        Action:
            - Sends a random number between 1 and the number of sides.
        """
        random_number_1 = random.randint(1, sides)
        random_number_2 = random_number_1

        # As long as random_number_1 is equal to random_number_2, we rethrow it
        while random_number_1 == random_number_2:
            random_number_2 = random.randint(1, sides)

        await send_response_to_discord(
            target=interaction,
            content=STRINGS['fun']['roll_result'].format(
                first_result=random_number_1,
                second_result=random_number_2
            )
        )

        logging.info(
            f"-- {interaction.user.name} use /roll slash command for dice with {sides} sides. Result: {random_number_1}, {random_number_2}")


async def setup(bot):
    """Adds this cog to the given bot"""
    await bot.add_cog(FunCog(bot))
