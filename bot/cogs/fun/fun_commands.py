"""Commands cog for fun slash commands.

Contains commands for quote member, roll dice, repeat user message
and respond to quoi commands.

© by hassanpacary
"""

# --- Forward references ---
from __future__ import annotations

# --- Standard library ---
import logging
from typing import TYPE_CHECKING

# --- Third-party ---
import discord
from discord import app_commands
from discord.ext import commands

# --- Internal ---
from bot.cogs.fun import fun_config, fun_strings
from bot.services.fun import fun_service, quote_service

if TYPE_CHECKING:
    from bot.core import bot as b


class FunCommands(commands.Cog):
    """Cog containing fun slash commands.

    Attributes:
        bot: The custom Discord bot instance.
    """

    def __init__(self, bot: b.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name=fun_config.Quoi.NAME,
        description=fun_config.Quoi.DESCRIPTION,
    )
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def quoi_command(self, interaction: discord.Interaction) -> None:
        """Responds to quoi slash command.

        Responds to user interaction with 'feur'.

        Args:
            interaction: The Discord interaction context.
        """
        logging.info(
            "%s used /quoi slash command",
            interaction.user.name,
        )
        await interaction.response.send_message(content=fun_strings.QUOI_RESPONSE)

    @app_commands.command(
        name=fun_config.Quote.NAME,
        description=fun_config.Quote.DESCRIPTION,
    )
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def quote_command(
        self,
        interaction: discord.Interaction,
        screen: discord.Attachment,
    ) -> None:
        """Responds to quote slash command.

        Exposing guild member with a screenshot in the quote channel.

        Args:
            interaction: The Discord interaction context.
            screen: The screenshot attachment to quote (required).
        """
        logging.info(
            "%s used /quote slash command",
            interaction.user.name,
        )
        await quote_service.quote_user_by_screenshot(
            interaction=interaction,
            screen=screen,
        )

    @app_commands.command(
        name=fun_config.Roll.NAME,
        description=fun_config.Roll.DESCRIPTION,
    )
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def roll_command(
        self,
        interaction: discord.Interaction,
        sides: app_commands.Range[int, 2, None] = 6,
    ) -> None:
        """Responds to roll slash command.

        Rolling dice with multiple face (min 2, default 6).

        Args:
            interaction: The Discord interaction context.
            sides: Number of sides on the dice (Defaults to 6).
        """
        logging.info(
            "%s used /roll slash command for a %s-sided dice",
            interaction.user.name,
            sides,
        )
        await fun_service.roll_dice(interaction=interaction, sides=sides)

    @app_commands.command(
        name=fun_config.Say.NAME,
        description=fun_config.Say.DESCRIPTION,
    )
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def say_command(
        self,
        interaction: discord.Interaction,
        message: str,
    ) -> None:
        """Responds to say slash command.

        Repeating a message in the same channel.
        The bot has 50% chance of revealing the author message.

        Args:
            interaction: The Discord interaction context.
            message: The message to repeat (required).
        """
        logging.info(
            "%s used /say slash command to repeat: %s",
            interaction.user.name,
            message,
        )
        await fun_service.repeat_message(interaction=interaction, message=message)
