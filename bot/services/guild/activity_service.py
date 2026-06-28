"""Activity service for guild cog.

Manage logics functions for the rotation of bot activity task (bot Discord presence).
Selects a random activity: either a preset from config file or a random anime
fetched from AniList API.

© by hassanpacary
"""

# --- Forward references ---
from __future__ import annotations

# --- Standard library ---
import random
from typing import TYPE_CHECKING

# --- Third-party ---
import discord

# --- Internal ---
from bot.cogs.guild import guild_strings
from bot.api.anilist import anilist_api_requests

if TYPE_CHECKING:
    from bot.core import bot as b


def _build_watching_state(activity: dict) -> str:
    """Builds a formatted presence string for a watching AniList anime activity.

    Assembles episode count, average score, and genres into a single string.
    Missing or None fields are omitted.

    Args:
        activity: A dict of anime metadata from the AniList API.

    Returns:
        A formatted string,
        e.g. '12 épisodes | score moyen 85% | genres Action, Adventure'.
    """
    parts = []

    episodes = activity.get('episodes')
    if episodes is not None:
        if episodes == 1:
            ep_label = guild_strings.Activity.WatchingStateInfo.EPISODE
        else:
            ep_label = f"{guild_strings.Activity.WatchingStateInfo.EPISODE}s"
        parts.append(f"{episodes} {ep_label}")

    average_score = activity.get('averageScore')
    if average_score is not None:
        parts.append(
            f"{guild_strings.Activity.WatchingStateInfo.MEAN_SCORE} {average_score}%",
        )

    genres = activity.get('genres')
    if genres and isinstance(genres, list):
        if len(guild_strings.Activity.WatchingStateInfo.GENRE) == 1:
            genre_label = guild_strings.Activity.WatchingStateInfo.GENRE
        else:
            genre_label = f"{guild_strings.Activity.WatchingStateInfo.GENRE}s"
        parts.append(f"{genre_label} {', '.join(genres)}")

    return guild_strings.Activity.WatchingStateInfo.SEPARATOR.join(parts)


async def _pick_random_activity() -> tuple[str, str, str]:
    """Selects a random activity for the bot presence.

    Either fetches a random anime from AniList (watching) or picks a
    preset activity from the config (game, anime, etc.).

    Returns:
        A tuple of (activity_name, activity_type, activity_state).
    """

    # Set watching if
    if random.randint(0, 1):
        activity_type = "watching"

        # Pick an AniList anime if
        if random.randint(0, 1):
            activity = await anilist_api_requests.fetch_random_anime()
            activity_name = activity['title']['romaji']
            activity_state = _build_watching_state(activity=activity)

        # Pick a random anime from the preset animes activities else
        else:
            activity_name, activity_state = random.choice(
                guild_strings.Activity.PRESET_WATCHING,
            )

        return activity_name, activity_type, activity_state

    # Pick a random game from the preset games else
    activity_type = "game"
    activity_name, activity_state = random.choice(
        guild_strings.Activity.PRESET_GAME,
    )

    return activity_name, activity_type, activity_state


async def set_bot_activity(bot: b.Bot) -> None:
    """Applies a random activity to the bot Discord presence.

    Args:
        bot: The Discord bot instance.

    Raises:
        ValueError: If the activity type is not recognized.
    """
    activity_name, activity_type, activity_state = await _pick_random_activity()

    if activity_type == "game":
        activity = discord.Game(name=activity_name, state=activity_state)
    elif activity_type == "watching":
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name=activity_name,
            state=activity_state,
        )
    elif activity_type == "listening":
        activity = discord.Activity(
            type=discord.ActivityType.listening,
            name=activity_name,
        )
    else:
        raise ValueError(f"Unrecognized activity_type: '{activity_type}'")

    await bot.change_presence(activity=activity)
