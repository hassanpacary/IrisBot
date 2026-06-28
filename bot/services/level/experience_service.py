"""experience service for level cog.

Manage logics functions for granting experience on user by on_message event
(or giving admin-only command).

© by hassanpacary
"""

# --- Standard library ---
import random

# --- Third-party ---
import discord

# --- Internal ---
from bot.cogs.level import level_config, level_strings
from bot.utils import db_manager, discord_utils


def _calcul_next_level(level: int, next_level: int) -> int:
    """Calculate the XP required to reach the next level.

    Formula: next_level + (level * _XP_PER_LEVEL_MULTIPLIER)

    Args:
        level: The current level after leveling up.
        next_level: The previous XP threshold.

    Returns:
        The new XP threshold for the next level.
    """
    return int(
        next_level + (level * level_config.XP_PER_LEVEL_MULTIPLIER),
    )


async def _check_level_up(  # pylint: disable=too-many-arguments, too-many-positional-arguments
        ctx: discord.Message | discord.Interaction,
        db: db_manager.DatabaseManager,
        xp: int,
        level: int,
        next_level: int,
        user: discord.Member | discord.User,
) -> bool:
    """Checks if the user has leveled up and updates the database accordingly.

    Loops until XP is below the next level threshold, incrementing the level
    and recalculate the threshold each iteration.

    Args:
        ctx: The Discord message or interaction context.
        db: The database manager instance.
        xp: The user's current XP after the addition.
        level: The user's current level.
        next_level: The XP required to reach the next level.
        user: The Discord user or member being checked.

    Returns:
        True if the user leveled up at least once, False otherwise.
    """
    level_up = False

    while xp >= next_level:
        xp -= next_level
        level += 1
        next_level = _calcul_next_level(level=level, next_level=next_level)

        await db.execute(
            "update_level",
            xp,
            level,
            next_level,
            user.id,
        )

        level_up = True

    if level_up:
        if isinstance(ctx.channel, discord.TextChannel):
            channel = await discord_utils.get_channel_by_ctx(
                ctx=ctx,
                channel_id=ctx.channel.id,
            )
            await channel.send(
                content=level_strings.LEVEL_UP.format(
                    user=user.display_name,
                    level=level,
                )
            )

    return level_up


async def apply_xp(
        ctx: discord.Message | discord.Interaction,
        db: db_manager.DatabaseManager,
        user_id: int,
        xp_add: int,
        user: discord.Member | discord.User,
) -> None:
    """Fetches the user from DB, inserts if absent, applies XP and checks level up.

    Args:
        ctx: The Discord message or interaction context.
        db: The database manager instance.
        user_id: The Discord user ID to update.
        xp_add: The amount of XP to add.
        user: The Discord user or member instance.
    """
    user_db = await db.fetchall("fetch_all", user_id)

    if not user_db:
        await db.execute("insert_user", user_id)
        user_db = await db.fetchall("fetch_all", user_id)

    xp = int(user_db[0][1]) + xp_add
    level = user_db[0][2]
    next_level = user_db[0][3]

    level_up = await _check_level_up(
        ctx=ctx,
        db=db,
        xp=xp,
        level=level,
        next_level=next_level,
        user=user,
    )

    if not level_up:
        await db.execute("update_xp", xp, user_id)


async def grant_xp_on_message(
        message: discord.Message,
        db: db_manager.DatabaseManager,
) -> None:
    """Grants a random amount of XP to the message author.

    Called on every user message via on_message listener.

    Args:
        message: The incoming Discord message.
        db: The database manager instance.
    """
    xp_add = random.randint(1, level_config.RANDOM_XP_MAX)

    await apply_xp(
        ctx=message,
        db=db,
        user_id=message.author.id,
        xp_add=xp_add,
        user=message.author,
    )
