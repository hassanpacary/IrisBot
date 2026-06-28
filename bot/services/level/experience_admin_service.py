"""Level admin service for level cog.

Manage logics functions for admin-only commands.
Like give XP and reset XP/level commands.

© by hassanpacary
"""

# --- Standard library ---
import logging

# --- Third-party ---
import discord

# --- Internal ---
from bot.cogs.level import level_strings
from bot.services.level import experience_service
from bot.utils import db_manager


async def grant_xp_by_admin(
    interaction: discord.Interaction,
    db: db_manager.DatabaseManager,
    amount: int,
    user: discord.User,
) -> None:
    """Grants a specific amount of XP to a target user via admin command.

    Args:
        interaction: The Discord interaction context.
        db: The database manager instance.
        amount: The amount of XP to grant.
        user: The Discord user to receive the XP.
    """
    await experience_service.apply_xp(
        ctx=interaction,
        db=db,
        user_id=user.id,
        xp_add=amount,
        user=user,
    )

    await interaction.response.send_message(
        content=level_strings.GIVE_XP.format(
            amount=amount,
            user=user.mention,
        ),
        ephemeral=True,
    )

    logging.info(
        "Admin granted %s experiences to %s",
        amount,
        user.display_name,
    )


async def reset_user_level(
    interaction: discord.Interaction,
    db: db_manager.DatabaseManager,
    user: discord.User,
) -> None:
    """Resets the XP and level of a user to their initial values.

    Args:
        interaction: The Discord interaction context.
        db: The database manager instance.
        user: The Discord user whose level will be reset.

    Raises:
        ValueError: If the user is not in the database.
    """
    user_db = await db.fetchall("fetch_all", user.id)

    if not user_db:
        await interaction.response.send_message(
            content=level_strings.MEMBER_NOT_IN_DB,
            ephemeral=True,
        )
        raise ValueError(f"Reset failed, user {user.id} not found in database")

    await db.execute("update_level", 0, 0, 50, user.id)

    await interaction.response.send_message(
        content=level_strings.LEVEL_RESET.format(user=user.mention),
        ephemeral=True,
    )

    logging.info("Levels reset for user %s", user.id)
