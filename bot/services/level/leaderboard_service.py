"""Leaderboard service for level cog.

Manage logics functions for display users leaderboard of the guild.

© by hassanpacary
"""

# --- Standard library ---
import logging

# --- Third-party ---
import discord

# --- Internal ---
from bot.cogs.level import level_config
from bot.services.level import leaderboard_view
from bot.utils import db_manager


def _paginate(data: list, page_size: int) -> list[list]:
    """Splits a list into pages of a given size.

    Args:
        data: The flat list to paginate.
        page_size: The maximum number of items per page.

    Returns:
        A list of pages, each being a sublist of at most page_size items.
    """
    return [data[i:i + page_size] for i in range(0, len(data), page_size)]


async def display_leaderboard(
        interaction: discord.Interaction,
        db: db_manager.DatabaseManager,
) -> None:
    """Displays a paginated leaderboard embed with navigation buttons.

    Args:
        interaction: The Discord interaction context.
        db: The database manager instance.
    """
    leaderboard_data = await db.fetchall("fetch_leaderboard")

    pages = _paginate(
        data=list(leaderboard_data),
        page_size=level_config.Leaderboard.LEADERBOARD_PAGE_SIZE
    )
    view = leaderboard_view.LeaderboardView(
        ctx=interaction,
        pages=pages,
        author=interaction.user,
    )
    embed = await view.get_embed()

    await interaction.response.send_message(embed=embed, view=view)

    logging.info("Leaderboard displayed with success")
