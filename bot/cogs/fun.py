"""
bot/cogs/fun.py
© by hassanpacary

Cog containing fun slash commands and their logic
"""

# --- Imports ---
import logging

# --- Third party imports ---
import discord
from discord import app_commands
from discord.ext import commands

# --- Bot modules ---
from bot.core.config_loader import BOT, COMMANDS, STRINGS, REGEX
from bot.services.fun.fun_service import roll_dice, repeat_message
from bot.services.fun.quote_component import quote_user_with_screen, quote_user_with_reaction
from bot.utils.discord_utils import send_response_to_discord
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

    # ███████╗██╗   ██╗███████╗███╗   ██╗████████╗███████╗
    # ██╔════╝██║   ██║██╔════╝████╗  ██║╚══██╔══╝██╔════╝
    # █████╗  ██║   ██║█████╗  ██╔██╗ ██║   ██║   ███████╗
    # ██╔══╝  ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║   ██║   ╚════██║
    # ███████╗ ╚████╔╝ ███████╗██║ ╚████║   ██║   ███████║
    # ╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝

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
        response = STRINGS['fun']['quoi']

        if matches_pattern(pattern, message.content):
            logging.info(
                "-- %s said: %s and matched with 'quoi' pattern",
                message.author,
                message.content
            )
            await send_response_to_discord(ctx=message, content=response)

        await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """
        Event listener that triggers whenever a reaction is added to a message

        Parameters:
            payload (discord.RawReactionActionEvent): The message who trigger the listener

        Actions:
            - Checks if the reaction added matche with the quote emoji
            - If found, quote the message
        """
        emoji = BOT['fun']['reaction_for_quote']
        if payload.emoji.name == emoji:
            await quote_user_with_reaction(ctx=self.bot, payload=payload)

    #  ██████╗ ██████╗ ███╗   ███╗███╗   ███╗ █████╗ ███╗   ██╗██████╗ ███████╗
    # ██╔════╝██╔═══██╗████╗ ████║████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝
    # ██║     ██║   ██║██╔████╔██║██╔████╔██║███████║██╔██╗ ██║██║  ██║███████╗
    # ██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║  ██║╚════██║
    # ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║██████╔╝███████║
    #  ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝

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
        response = STRINGS['fun']['quoi']

        logging.info(
            "-- %s use /quoi slash command",
            interaction.user.name
        )
        await send_response_to_discord(ctx=interaction, content=response)

    @app_commands.command(
        name=COMMANDS['fun']['quote']['slash_command'],
        description=COMMANDS['fun']['quote']['description'],
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def quote_logic(self, interaction: discord.Interaction, screen: discord.Attachment):
        """
        Responds to the /quote slash command

        Parameters:
            interaction (discord.Interaction): The interaction object triggered by the user
            screen (discord.Attachment): The screen for quote user

        Action:
            - Send the quote of the user with a screen
        """

        logging.info(
            "-- %s use /quote slash command",
            interaction.user.name
        )
        await quote_user_with_screen(ctx=interaction, screen=screen)

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
            - Sends a random number between 1 and the number of sides
        """
        logging.info(
            "-- %s use /roll slash command for dice with %s sides",
            interaction.user.name,
            sides
        )
        await roll_dice(ctx=interaction, sides=sides)

    @app_commands.command(
        name=COMMANDS['fun']['say']['slash_command'],
        description=COMMANDS['fun']['say']['description'],
    )
    @app_commands.allowed_contexts(guilds=True)
    async def say_logic(self, interaction: discord.Interaction, message: str):
        """
        Responds to the /say slash command

        Parameters:
            interaction (discord.Interaction): The interaction object triggered by the user
            message (str): The message to repeat

        Action:
            - Repeat the message in chat in a detached message
        """
        logging.info(
            "-- %s use /say slash command for repeat %s",
            interaction.user.name,
            message
        )
        await repeat_message(ctx=interaction, message=message)


async def setup(bot):
    """Adds this cog to the given bot"""
    await bot.add_cog(FunCog(bot))
