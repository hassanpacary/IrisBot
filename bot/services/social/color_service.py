"""Custom color service for social cog.

Manage logics functions for select a custom color as guild user.

© by hassanpacary
"""

# --- Standard library ---
import logging
import re
from typing import cast

# --- Third-party ---
import discord

# --- Internal ---
from bot.cogs.social import social_config, social_strings
from bot.config import regex_config
from bot.utils import db_manager


async def _create_color_role(
        interaction: discord.Interaction,
        db: db_manager.DatabaseManager,
        role_name: str,
        hex_value: str,
) -> None:
    """Creates and assigns a custom color role to the user.

    If the user already has a color role in the database, the old role
    is deleted and replaced with the new one.

    Args:
        interaction: The Discord interaction context.
        db: The color database manager instance.
        role_name: The name of the role to create.
        hex_value: The hex color value (with or without leading '#').

    Raises:
        ValueError: If no ctx guild was found for the interaction.
        ValueError: If no ctx member was found for the interaction.
    """
    guild = interaction.guild
    member = cast(discord.Member, interaction.user)
    color = (
        discord.Color.from_str(hex_value)
        if hex_value.startswith("#")
        else discord.Color(int(hex_value, 16))
    )

    if not guild:
        raise ValueError("No guild found for the interaction.")

    if not member:
        raise ValueError("No member found for the interaction.")

    created_role = await guild.create_role(name=role_name, color=color)

    position_role = guild.get_role(
        social_config.Color.COLOR_ROLE_ID_POSITION,
    )
    if position_role is not None:
        await guild.edit_role_positions(
            positions={created_role: position_role.position - 1}
        )

    color_db = await db.fetchall("fetch_all", member.id)
    if not color_db:
        await db.execute(
            "insert_color",
            member.id,
            created_role.id,
        )
    else:
        old_role = guild.get_role(color_db[0][1])
        if old_role is not None:
            await old_role.delete(reason=social_strings.Color.DELETE_REASON)
        await db.execute(
            "update_color",
            created_role.id,
            member.id,
        )

    await member.add_roles(
        created_role,
        reason=social_strings.Color.CREATE_REASON)

    await interaction.response.send_message(
        content=social_strings.Color.WITH_SUCCESS,
        ephemeral=True,
    )

    logging.info(
        "%s created color role '%s' (%s)",
        member.name,
        role_name,
        hex_value,
    )


async def check_ability_of_use_color_command(
        interaction: discord.Interaction,
        color_db: db_manager.DatabaseManager,
        level_db: db_manager.DatabaseManager,
        role_name: str,
        hex_value: str,
) -> None:
    """Checks the user's level and validates the hex value,
    if all conditions are met call _create_color_role functions.

    Args:
        interaction: The Discord interaction context.
        color_db: The color database manager instance.
        level_db: The level database manager instance.
        role_name: The name of the color role to create.
        hex_value: The hex color value (with or without leading '#').
    """
    user_db = await level_db.fetchall("fetch_all", interaction.user.id)
    user_level = user_db[0][2] if user_db else 0

    if user_level < social_config.Color.LEVEL_FOR_USE_COLOR_COMMAND:
        await interaction.response.send_message(
            content=social_strings.Color.LEVEL_NOT_REACHED,
            ephemeral=True,
        )
        return

    if not re.match(pattern=regex_config.HEX_COLOR_VALUE, string=hex_value):
        await interaction.response.send_message(
            content=social_strings.Color.INVALID_HEX,
            ephemeral=True,
        )
        return

    await _create_color_role(
        interaction=interaction,
        db=color_db,
        role_name=role_name,
        hex_value=hex_value,
    )
