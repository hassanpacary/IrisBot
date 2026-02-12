"""
bot/services/level/level_service.py
© by hassanpacary

Utility functions for bot leveling tasks
"""

# --- Imports ---
import random

# --- Third party imports ---
import discord
from discord.utils import MISSING

# --- Bot modules ---
from bot.core.config_loader import BOT, STRINGS
from bot.services.level.leaderboard_view import LeaderboardView
from bot.utils.db_manager import DatabaseManager
from bot.utils.discord_utils import send_response_to_discord


# ██╗     ███████╗██╗   ██╗███████╗██╗     ██╗███╗   ██╗ ██████╗
# ██║     ██╔════╝██║   ██║██╔════╝██║     ██║████╗  ██║██╔════╝
# ██║     █████╗  ██║   ██║█████╗  ██║     ██║██╔██╗ ██║██║  ███╗
# ██║     ██╔══╝  ╚██╗ ██╔╝██╔══╝  ██║     ██║██║╚██╗██║██║   ██║
# ███████╗███████╗ ╚████╔╝ ███████╗███████╗██║██║ ╚████║╚██████╔╝
# ╚══════╝╚══════╝  ╚═══╝  ╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝


async def _check_level_up(
        ctx: discord.Message|discord.Interaction,
        db: DatabaseManager,
        xp: int,
        level: int,
        next_level: int,
        target_user: discord.User = MISSING,
):
    """
    Check and update the current level and amound of XP of the user

    Parameters:
        ctx (discord.Message): the discord message
        db (DatabaseManager): the database manager
        xp (int): the current level
        level (int): the current level
        next_level (int): the next level
        target_user (discord.User|None): the user to check (context: giving xp)
    """
    response = STRINGS['level']['level_up']
    next_level_calcul = BOT['level']['level_up_calcul']

    if isinstance(ctx, discord.Message):
        user = ctx.author
    else:
        user = target_user

    level_up = False
    while xp >= next_level:
        xp = xp - next_level
        level += 1
        next_level = int(eval(next_level_calcul, {"level": level, "next_level": next_level}))

        await db.execute("update_level", xp, level, next_level, user.id)

        level_up = True

    if level_up:
        await send_response_to_discord(
            ctx=ctx,
            content=response.format(user=user.display_name, level=level),
            detach=True
        )

    return level_up


async def update_xp_nd_level(
        ctx: discord.Message|discord.Interaction,
        db: DatabaseManager,
        amount: int = None,
        target_user: discord.User = MISSING
):
    """logic of level and xp update"""
    random_xp_max = BOT['level']['random_xp_max']

    if isinstance(ctx, discord.Message):
        user = ctx.author.id
        xp_add = random.randint(1, random_xp_max)
    else:
        user = target_user
        xp_add = amount

    user_db = await db.fetchall("fetch_all", user)

    if not user_db:
        await db.execute("insert_user", user)
        user_db = await db.fetchall("fetch_all", user)

    xp = user_db[0][1] + xp_add
    level = user_db[0][2]
    next_level = user_db[0][3]

    if isinstance(ctx, discord.Message):
        level_up = await _check_level_up(
            ctx=ctx,
            db=db,
            xp=xp,
            level=level,
            next_level=next_level
        )
    else:
        level_up = await _check_level_up(
            ctx=ctx,
            db=db,
            xp=xp,
            level=level,
            next_level=next_level,
            target_user=user
        )

    if not level_up:
        await db.execute("update_xp", xp, user)

    # Message when admin give xp to a user
    response = STRINGS['level']['cheating']
    if isinstance(ctx, discord.Interaction):
        await send_response_to_discord(
            ctx=ctx,
            content=response.format(amount=amount, user=user.mention),
        )


async def reset_user_level(ctx: discord.Interaction, db: DatabaseManager, user: discord.User):
    """logic of reset user"""
    response = STRINGS['level']['reset_user']

    user_id = user.id
    user_db = await db.fetchall("fetch_all", user_id)

    if not user_db:
        await send_response_to_discord(
            ctx=ctx,
            content=STRINGS['level']['not_reset_user'],
            ephemeral=True
        )
    else:
        await db.execute("update_level", 0, 0, 50, user.id)

        await send_response_to_discord(
            ctx=ctx,
            content=response.format(user=user.mention),
            ephemeral=True
        )



# ██╗     ███████╗ █████╗ ██████╗ ███████╗██████╗ ██████╗  ██████╗  █████╗ ██████╗ ██████╗
# ██║     ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔══██╗
# ██║     █████╗  ███████║██║  ██║█████╗  ██████╔╝██████╔╝██║   ██║███████║██████╔╝██║  ██║
# ██║     ██╔══╝  ██╔══██║██║  ██║██╔══╝  ██╔══██╗██╔══██╗██║   ██║██╔══██║██╔══██╗██║  ██║
# ███████╗███████╗██║  ██║██████╔╝███████╗██║  ██║██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝
# ╚══════╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝


def _paginate(data: list, page_size: int = 10) -> list[list]:
    """
    Paginate a list of sized list

    Parameters:
        - data (list): the list of data
        - page_size (int): the page size

    Returns:
        - list: the list of paginated data
    """
    return [data[i:i + page_size] for i in range(0, len(data), page_size)]


async def get_leaderboard(ctx: discord.Interaction, db: DatabaseManager):
    responses_dict = STRINGS['level']['leaderboard']

    leaderboard_data = await db.fetchall("fetch_leaderboard")
    if leaderboard_data is None:
        await send_response_to_discord(ctx=ctx, content=responses_dict['no_leaderboard'])
        return

    pages = _paginate(leaderboard_data)
    view = LeaderboardView(ctx=ctx, pages=pages, author=ctx.user)
    leaderboard = await view.get_embed()

    await send_response_to_discord(ctx=ctx, embed=leaderboard, view=view)
