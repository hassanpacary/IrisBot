"""
bot/services/bot/activity_component.py
© by hassanpacary

Utility functions to manage Discord bot activities (presence)
"""

# --- Imports ---
import random

# --- Third party imports ---
import discord
from discord.ext import commands

# --- Bot modules ---
from bot.core.config_loader import STRINGS
from bot.services.guild.anilist_api_service import fetch_random_anime


# ██████╗  ██████╗ ████████╗     █████╗  ██████╗████████╗██╗██╗   ██╗██╗████████╗██╗   ██╗
# ██╔══██╗██╔═══██╗╚══██╔══╝    ██╔══██╗██╔════╝╚══██╔══╝██║██║   ██║██║╚══██╔══╝╚██╗ ██╔╝
# ██████╔╝██║   ██║   ██║       ███████║██║        ██║   ██║██║   ██║██║   ██║    ╚████╔╝
# ██╔══██╗██║   ██║   ██║       ██╔══██║██║        ██║   ██║╚██╗ ██╔╝██║   ██║     ╚██╔╝
# ██████╔╝╚██████╔╝   ██║       ██║  ██║╚██████╗   ██║   ██║ ╚████╔╝ ██║   ██║      ██║
# ╚═════╝  ╚═════╝    ╚═╝       ╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═══╝  ╚═╝   ╚═╝      ╚═╝


async def _watching_state_constructor(activity: dict) -> str:
    """
    Construct a formatted state string from a bot dictionary

    Parameters:
        activity (dict): A dictionary containing information about the bot

    Returns:
        str: A formatted string describing the bot state
             Example: "12 épisodes | score moyen 85% | genres Action, Adventure"
    """
    informations_dict = STRINGS['guild']['activity_component']['watching_state_informations']

    state_parts = []

    # --- Episodes counts ---
    if "episodes" in activity and activity['episodes'] is not None:
        if activity['episodes'] == 1:
            episodes_info = (
                f"{activity['episodes']} "
                f"{informations_dict['episode']}"
            )
        else:
            episodes_info = (
                f"{activity['episodes']} "
                f"{informations_dict['episode']}s"
            )
        state_parts.append(episodes_info)

    # --- Mean score exist ---
    if "averageScore" in activity and activity['averageScore'] is not None:
        state_parts.append(
            f"{informations_dict['mean_score']} "
            f"{activity['averageScore']}%"
        )

    # --- Genres counts ---
    if "genres" in activity and activity['genres']:
        if len(activity['genres']) == 1:
            genres_info = (
                f"{informations_dict['genre']} "
                f"{', '.join(activity['genres'])}"
            )
        else:
            genres_info = (
                f"{informations_dict['genre']}s "
                f"{', '.join(activity['genres'])}"
            )
        state_parts.append(genres_info)

    return " | ".join(state_parts)


async def _random_activity() -> tuple[str, str, str]:
    """
    Generates a random bot for the bot's presence

    Depending on a random choice, the bot can either be:
    1. A randomly selected anime from AniList
    2. A preset bot defined in the strings JSON configuration

    Returns:
        tuple[
        activity_name (str): The display name of the bot,
        activity_type (str): The type of bot, e.g., "watching" or "game",
        activity_state (str): Optional state/description associated with the bot
        ]
    """
    preset_activities_dict = STRINGS['guild']['activity_component']['preset_activity']

    random_swap = random.randint(0, 1)

    # --- Watch random anilist anime ---
    if random_swap:
        activity = await fetch_random_anime()
        activity_type = "watching"
        activity_name = activity['title']['romaji']
        activity_state = await _watching_state_constructor(activity)

    # --- Random preset bot --
    else:
        activity_type, activity_list = random.choice(list(preset_activities_dict.items()))
        activity = random.choice(list(activity_list))
        activity_name = activity['activity_name']
        activity_state = activity['activity_state']

    return activity_name, activity_type, activity_state


async def set_bot_activity(ctx: commands.Bot):
    """
    Change the bot's Discord bot (presence) in a standardized way

    Parameters:
        ctx (commands.Bot): The bot instance
    """
    activity_name, activity_type, activity_state = await _random_activity()

    # --- Play game ---
    if activity_type == "game":
        activity = discord.Game(name=activity_name, state=activity_state)

    # --- Watching video ---
    elif activity_type == "watching":
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name=activity_name,
            state=activity_state
        )

    # --- Listening music ---
    elif activity_type == "listening":
        activity = discord.Activity(type=discord.ActivityType.listening, name=activity_name)

    else:
        raise ValueError(f"Invalid activity_type: {activity_type}")

    await ctx.change_presence(activity=activity)
