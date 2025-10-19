"""
bot/services/level/level_service.py
© by hassanpacary

Utility functions for bot leveling tasks
"""
import random

# --- Third party imports ---
import discord

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
        ctx: discord.Message,
        db: DatabaseManager,
        xp: int,
        level: int,
        next_level: int
):
    """
    Check and update the current level and amound of XP of the user

    Parameters:
        - ctx (discord.Message): the discord message
        - db (DatabaseManager): the database manager
        - xp (int): the current level
        - level (int): the current level
        - next_level (int): the next level
    """
    response = STRINGS['level']['level_up']
    next_level_calcul = BOT['level']['level_up_calcul']

    author = ctx.author.id

    if xp >= next_level:
        xp = xp - next_level
        level += 1
        next_level = int(eval(next_level_calcul, {"level": level, "next_level": next_level}))

        await db.execute("update_xp", xp, author)
        await db.execute("update_level", level, next_level, author)

        await send_response_to_discord(
            ctx=ctx,
            content=response.format(user=ctx.author.display_name, level=level),
            detach=True
        )

        return True

    return False


async def update_level(ctx: discord.Message, db: DatabaseManager):
    """logic of level and xp update"""
    random_xp_max = BOT['level']['random_xp_max']

    author = ctx.author.id

    user_db = await db.fetchall("fetch_all", author)

    if not user_db:
        await db.execute("insert_user", author)
        user_db = await db.fetchall("fetch_all", author)

    xp = user_db[0][1]
    level = user_db[0][2]
    next_level = user_db[0][3]

    # add xp for the message
    xp += random.randint(1, random_xp_max)

    level_up = await _check_level_up(
        ctx=ctx,
        db=db,
        xp=xp,
        level=level,
        next_level=next_level
    )

    if not level_up:
        await db.execute("update_xp", xp, author)


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
