"""Fun service for fun cog.

Manage logics functions for quoi, roll and repeat commands.

© by hassanpacary
"""

# --- Standard library ---
import logging
import random

# --- Third-party ---
import discord
from discord import TextChannel

# --- Internal ---
from bot.cogs.fun import fun_strings


async def handle_quoi_message(message: discord.Message) -> None:
    """Replies 'feur' if the message content matches the 'quoi' pattern.

    Args:
        message: The incoming Discord message to evaluate.
    """
    await message.channel.send(content=fun_strings.QUOI_RESPONSE)
    logging.info(
        "%s said: '%s' and matched with 'quoi' pattern.",
        message.author,
        message.content,
    )


async def roll_dice(interaction: discord.Interaction, sides: int) -> None:
    """Rolls dice with the given number of sides and replies with the results.

    Args:
        interaction: The Discord interaction context.
        sides: Number of sides on each dice.
    """
    result = random.randint(1, sides)

    await interaction.response.send_message(
        content=fun_strings.ROLL_RESULT.format(result=result),
    )

    logging.info(
        "%s rolled a %s-sided dice: %s",
        interaction.user.name,
        sides,
        result,
    )


async def repeat_message(
    interaction: discord.Interaction,
    message: str,
) -> None:
    """Repeats the given message in the channel as the bot.

    Sends the message directly to the channel so it appears as if
    the bot said it unprompted with 50% chance to disclose the command author.

    Args:
        interaction: The Discord interaction context.
        message: The message string to repeat.
    """
    assert isinstance(interaction.channel, TextChannel)

    await interaction.channel.send(content=message)

    random_swap = random.randint(0, 1)
    if random_swap:
        await interaction.response.send_message(
            content=fun_strings.Say.WITH_SOURCE.format(user=interaction.user.mention),
        )
    else:
        await interaction.response.send_message(
            content=fun_strings.Say.WITH_SUCCESS,
            ephemeral=True,
        )

    logging.info(
        "Message sends by %s repeat with success: %s",
        interaction.user.name,
        message,
    )
