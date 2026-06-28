"""Guild admin service for guild cog.

Manage logics functions for admin-only commands. Like purge channel command.

© by hassanpacary
"""

# --- Standard library ---
import logging

# --- Third-party ---
import discord
from discord import TextChannel

# --- Internal ---
from bot.cogs.guild import guild_config, guild_strings


async def purge(interaction: discord.Interaction, amount: int) -> None:
    """Purges a given number of messages from the current channel.

    Args:
        interaction: The Discord interaction context.
        amount: The number of messages to delete.
    """
    assert isinstance(interaction.channel, TextChannel)

    if amount <= 0:
        await interaction.response.send_message(
            content=guild_strings.Purge.AMOUNT_TOO_LOW,
            ephemeral=True,
        )
        return

    max_amount = guild_config.AdminCommands.Purge.PURGE_AMOUNT_MAX
    if amount > max_amount:
        await interaction.response.send_message(
            content=guild_strings.Purge.AMOUNT_TOO_HIGH.format(
                max=max_amount,
            ),
            ephemeral=True,
        )
        return

    await interaction.response.defer(ephemeral=True)
    await interaction.channel.purge(limit=amount)
    await interaction.followup.send(
        guild_strings.Purge.WITH_SUCCESS.format(amount=str(amount)),
        ephemeral=True,
    )

    logging.info(
        "%s purged %s message(s) in #%s",
        interaction.user.name,
        amount,
        interaction.channel,
    )
