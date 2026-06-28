"""Core service for core bot configuration.

Manage logics functions for database initialization
and Discord intents configuration.

© by hassanpacary
"""

# --- Forward references ---
from __future__ import annotations

# --- Standard library ---
import logging
from typing import TYPE_CHECKING

# --- Third-party ---
import discord

# --- Internal ---
from bot.config import bot_config

if TYPE_CHECKING:
    from bot.core import bot as b


def build_intents() -> discord.Intents:
    """Builds a discord.Intents instance from bot_config.py.

    Only recognized intent names are applied, unknown keys are silently
    ignored to avoid AttributeError on invalid config entries.

    Returns:
        A configured discord.Intents instance.
    """
    intents = discord.Intents.default()
    for name, enabled in bot_config.INTENTS.items():
        if hasattr(intents, name):
            setattr(intents, name, enabled)
    return intents


async def init_databases(bot: b.Bot) -> None:
    """Connects to db and initializes all bot databases.

    Creates the required tables if they do not already exist.
    Called from setup_hook before any cog accesses the DBs.

    Args:
        bot: A bot instance exposing color_db and level_db managers.
    """
    await bot.colors_db.connect()
    bot.colors_db.load_queries(filename="colors.sql")
    await bot.colors_db.execute(query_name="create_table_colors")

    await bot.levels_db.connect()
    bot.levels_db.load_queries(filename="levels.sql")
    await bot.levels_db.execute(query_name="create_table_levels")

    logging.info("Databases initialized successfully")
