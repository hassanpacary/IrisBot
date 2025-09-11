"""
bot/utils/activity_service.py
© by hassanpacary

Utility functions to manage Discord bot activities (presence).
"""

# --- Imports ---
import random
from typing import Optional

# --- Third party imports ---
import discord
from discord.ext import commands

# --- Bot modules ---
from bot.core.config_loader import STRINGS
from bot.services.anilist_service import fetch_random_anime


# ██████╗  ██████╗ ████████╗     █████╗  ██████╗████████╗██╗██╗   ██╗██╗████████╗██╗   ██╗
# ██╔══██╗██╔═══██╗╚══██╔══╝    ██╔══██╗██╔════╝╚══██╔══╝██║██║   ██║██║╚══██╔══╝╚██╗ ██╔╝
# ██████╔╝██║   ██║   ██║       ███████║██║        ██║   ██║██║   ██║██║   ██║    ╚████╔╝
# ██╔══██╗██║   ██║   ██║       ██╔══██║██║        ██║   ██║╚██╗ ██╔╝██║   ██║     ╚██╔╝
# ██████╔╝╚██████╔╝   ██║       ██║  ██║╚██████╗   ██║   ██║ ╚████╔╝ ██║   ██║      ██║
# ╚═════╝  ╚═════╝    ╚═╝       ╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═══╝  ╚═╝   ╚═╝      ╚═╝


async def set_bot_activity(
        bot: commands.Bot,
        activity_name: str,
        activity_type: str = "watching",
        activity_state: Optional[str] = None,
        url: Optional[str] = None
) -> None:
    """
    Change the bot's Discord activity (presence) in a standardized way.

    Args:
        bot (commands.Bot): The bot instance.
        activity_name (str): Name of the activity (e.g., game title or anime name).
        activity_type (Literal["game", "watching", "listening", "streaming"]):
            Type of the activity. Defaults to 'watching'.
        activity_state (Optional[str]): Optional detailed state/description.
        url (Optional[str]): Optional URL for streaming activity.

    Usage:
        await set_bot_activity(bot, "Minecraft", "game")
        await set_bot_activity(bot, "Anime XYZ", "watching", "Episode 10")
        await set_bot_activity(bot, "Music Stream", "streaming", url="https://twitch.tv/xyz")
    """

    # --- Play game ---
    if activity_type == "game":
        activity = discord.Game(name=activity_name, state=activity_state)

    # --- Watching video ---
    elif activity_type == "watching":
        activity = discord.Activity(type=discord.ActivityType.watching, name=activity_name, state=activity_state)

    # --- Listening music ---
    elif activity_type == "listening":
        activity = discord.Activity(type=discord.ActivityType.listening, name=activity_name)

    # --- Stream ---
    elif activity_type == "streaming":
        activity = discord.Streaming(name=activity_name, url=url or "", state=activity_state)

    else:
        raise ValueError(f"Invalid activity_type: {activity_type}")

    await bot.change_presence(activity=activity)


#  ██████╗ ██████╗ ███╗   ██╗███████╗████████╗██████╗ ██╗   ██╗ ██████╗████████╗ ██████╗ ██████╗
# ██╔════╝██╔═══██╗████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║   ██║██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
# ██║     ██║   ██║██╔██╗ ██║███████╗   ██║   ██████╔╝██║   ██║██║        ██║   ██║   ██║██████╔╝
# ██║     ██║   ██║██║╚██╗██║╚════██║   ██║   ██╔══██╗██║   ██║██║        ██║   ██║   ██║██╔══██╗
# ╚██████╗╚██████╔╝██║ ╚████║███████║   ██║   ██║  ██║╚██████╔╝╚██████╗   ██║   ╚██████╔╝██║  ██║
#  ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝  ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝


async def watching_state_constructor(activity: dict) -> str:
    """
    Construct a formatted state string from an activity dictionary.

    The function combines different pieces of metadata about an anime
    Each available element is appended to the final string, separated by " | ".

    Args:
        activity (dict): A dictionary containing information about the activity.

    Returns:
        str: A formatted string describing the activity state.
             Example: "12 épisodes | score moyen 85% | genres Action, Adventure"
    """
    # --- Load strings for watching state
    watching_state_informations = STRINGS['event']['status_activity']['watching_state_informations']

    state_parts = []

    # --- Episodes counts ---
    if "episodes" in activity and activity['episodes'] is not None:
        if activity['episodes'] == 1:
            episodes_info = (
                f"{activity['episodes']} "
                f"{watching_state_informations['episode']}"
            )
        else:
            episodes_info = (
                f"{activity['episodes']} "
                f"{watching_state_informations['episode']}s"
            )
        state_parts.append(episodes_info)

    # --- Mean score exist ---
    if "averageScore" in activity and activity['averageScore'] is not None:
        state_parts.append(
            f"{watching_state_informations['mean_score']} "
            f"{activity['averageScore']}%"
        )

    # --- Genres counts ---
    if "genres" in activity and activity['genres']:
        if len(activity['genres']) == 1:
            genres_info = (
                f"{watching_state_informations['genre']} "
                f"{', '.join(activity['genres'])}"
            )
        else:
            genres_info = (
                f"{watching_state_informations['genre']}s "
                f"{', '.join(activity['genres'])}"
            )
        state_parts.append(genres_info)

    return " | ".join(state_parts)


# ██████╗  █████╗ ███╗   ██╗██████╗  ██████╗ ███╗   ███╗     █████╗  ██████╗████████╗██╗██╗   ██╗██╗████████╗██╗   ██╗
# ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██╔═══██╗████╗ ████║    ██╔══██╗██╔════╝╚══██╔══╝██║██║   ██║██║╚══██╔══╝╚██╗ ██╔╝
# ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║██╔████╔██║    ███████║██║        ██║   ██║██║   ██║██║   ██║    ╚████╔╝
# ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║██║╚██╔╝██║    ██╔══██║██║        ██║   ██║╚██╗ ██╔╝██║   ██║     ╚██╔╝
# ██║  ██║██║  ██║██║ ╚████║██████╔╝╚██████╔╝██║ ╚═╝ ██║    ██║  ██║╚██████╗   ██║   ██║ ╚████╔╝ ██║   ██║      ██║
# ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝  ╚═════╝ ╚═╝     ╚═╝    ╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═══╝  ╚═╝   ╚═╝      ╚═╝


async def random_activity() -> tuple[str, str, str]:
    """
    Generates a random activity for the bot's presence.

    Depending on a random choice, the activity can either be:
    1. A randomly selected anime from AniList.
    2. A preset activity defined in the strings JSON configuration.

    Returns:
        tuple[str, str, str]:
            - activity_name (str): The display name of the activity.
            - activity_type (str): The type of activity, e.g., "watching" or "game".
            - activity_state (str): Optional state/description associated with the activity.
    """
    preset_activities = STRINGS['event']['status_activity']['preset_activity']

    random_swap = random.randint(0, 1)

    # --- Watch random anilist anime ---
    if random_swap:
        activity = await fetch_random_anime()
        activity_type = "watching"
        activity_name = activity['title']['romaji']
        activity_state = await watching_state_constructor(activity)

    # --- Random preset activity --
    else:
        activity_type, activity_list = random.choice(list(preset_activities.items()))
        activity = random.choice(list(activity_list))
        activity_name = activity['activity_name']
        activity_state = activity['activity_state']

    return activity_name, activity_type, activity_state
