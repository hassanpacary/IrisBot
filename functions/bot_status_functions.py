"""
bot_status.py
© by hassanpacary

Useful functions for request the Anilist API to retrieve a random anime for the bot's status.
"""

# --- Imports ---
import datetime
import logging
import random

# --- Third party imports ---
import aiohttp

# --- Bot modules ---
from functions.functions import load_json, load_graphql_query

# Load config data from json files
config = load_json("config.json")
string = load_json(f"string_config_{config['config']['langage']}.json")

# --- Anilist API ---
API_URL = config['api']['anilist']['api_url']
HEADERS = config['api']['anilist']['api_header']


async def get_anilist_total_anime() -> int:
    """
    Fetches the total number of anime entries available on AniList.

    Actions:
        This function loads a GraphQL query from the 'queries/get_anilist_total_anime.graphql'
        file, sends it to the AniList API, and returns the total count of anime entries.

    Returns:
        int: The total number of anime entries listed on AniList.
             Returns -1 if the request fails or an error occurs during fetching.
    """
    query = await load_graphql_query('get_anilist_total_anime.graphql')

    # Request to anilist API for get total anime count
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, json={'query': query},headers=HEADERS) as resp:
                resp.raise_for_status()
                data = await resp.json()
                return data['data']['Page']['pageInfo']['total']
    except aiohttp.ClientError as e:
        logging.error(
            '%s -- Error: fetching total anilist anime count error: %s',
            datetime.datetime.now().strftime('%d.%m.%Y %T'), e
        )
        return -1


async def fetch_random_anime() -> dict:
    """
    Fetch a random anime title from AniList.

    Actions:
        This function first retrieves the total number of anime entries from AniList,
        calculates a random page, and then fetches a list of anime titles from that page.
        Finally, it selects and returns a random title from the list.

    Returns:
        str: A random anime title in Romaji if successful;
             an empty string if there was an error during the request.
    """
    total = await get_anilist_total_anime()

    if total == -1:
        return {}

    per_page = 25
    max_pages = (total // per_page) + 1
    random_page = random.randint(1, max_pages)

    query = await load_graphql_query('get_anilist_random_page.graphql')

    try:
        json_request = {'query': query, 'variables': {'page': random_page, 'perPage': per_page}}

        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, json=json_request,headers=HEADERS) as resp:
                resp.raise_for_status()
                data = await resp.json()
                return random.choice(data['data']['Page']['media'])
    except aiohttp.ClientError as e:
        logging.error(
            '%s -- Error: fetching a random anilist anime page: %s',
            datetime.datetime.now().strftime('%d.%m.%Y %T'), e
        )
        return {}


async def state_constructor(activity: dict) -> str:
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
    state_parts = []

    # --- Episodes counts ---
    if 'episodes' in activity and activity['episodes'] is not None:
        if activity['episodes'] == 1:
            episodes_info = (
                f"{activity['episodes']} "
                f"{string['event']['status_activity']['anilist_state_informations']['episode']}"
            )
        else:
            episodes_info = (
                f"{activity['episodes']} "
                f"{string['event']['status_activity']['anilist_state_informations']['episode']}s"
            )
        state_parts.append(episodes_info)

    # --- Mean score exist ---
    if 'averageScore' in activity and activity['averageScore'] is not None:
        state_parts.append(
            f"{string['event']['status_activity']['anilist_state_informations']['mean_score']} "
            f"{activity['averageScore']}%"
        )

    # --- Genres counts ---
    if 'genres' in activity and activity['genres']:
        if len(activity['genres']) == 1:
            genres_info = (
                f"{string['event']['status_activity']['anilist_state_informations']['genre']} "
                f"{', '.join(activity['genres'])}"
            )
        else:
            genres_info = (
                f"{string['event']['status_activity']['anilist_state_informations']['genre']}s "
                f"{', '.join(activity['genres'])}"
            )
        state_parts.append(genres_info)

    return " | ".join(state_parts)
