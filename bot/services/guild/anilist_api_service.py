"""
bot/services/bot/anilist_api_service.py
© by hassanpacary

Utility functions for fetching data from AniList API
"""

# --- Imports ---
import random
import os

# --- Bot modules ---
from bot.utils.aiohttp_client import aiohttp_client
from bot.utils.files_utils import load_file


# pylint: disable=line-too-long
#  █████╗ ███╗   ██╗██╗██╗     ██╗███████╗████████╗    ███████╗███████╗██████╗ ██╗   ██╗██╗ ██████╗███████╗
# ██╔══██╗████╗  ██║██║██║     ██║██╔════╝╚══██╔══╝    ██╔════╝██╔════╝██╔══██╗██║   ██║██║██╔════╝██╔════╝
# ███████║██╔██╗ ██║██║██║     ██║███████╗   ██║       ███████╗█████╗  ██████╔╝██║   ██║██║██║     █████╗
# ██╔══██║██║╚██╗██║██║██║     ██║╚════██║   ██║       ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██║██║     ██╔══╝
# ██║  ██║██║ ╚████║██║███████╗██║███████║   ██║       ███████║███████╗██║  ██║ ╚████╔╝ ██║╚██████╗███████╗
# ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚══════╝╚═╝╚══════╝   ╚═╝       ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚═╝ ╚═════╝╚══════╝
# pylint: enable=line-too-long


async def _get_api_endpoint() -> tuple[str, dict]:
    """
    Loads the AniList GraphQL endpoint URL and headers from env file

    Returns:
        tuple: (url: str, headers: dict)
    """
    al_api_url = os.environ["ANILIST_API_URL"]
    return al_api_url, {"Content-Type": "application/json"}


async def _load_graphql_query(query: str) -> str:
    """
    Load a GraphQL query file from the `queries` directory

    Returns:
        str: GraphQL query
    """
    query_file_path = os.path.join('bot', 'queries', query)

    # --- Read the query file ---
    return load_file(query_file_path, "r")


# ██████╗ ███████╗ ██████╗ ██╗   ██╗███████╗███████╗████████╗███████╗
# ██╔══██╗██╔════╝██╔═══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝██╔════╝
# ██████╔╝█████╗  ██║   ██║██║   ██║█████╗  ███████╗   ██║   ███████╗
# ██╔══██╗██╔══╝  ██║▄▄ ██║██║   ██║██╔══╝  ╚════██║   ██║   ╚════██║
# ██║  ██║███████╗╚██████╔╝╚██████╔╝███████╗███████║   ██║   ███████║
# ╚═╝  ╚═╝╚══════╝ ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝   ╚══════╝


async def _get_al_animes() -> int:
    """
    Fetch the total number of anime entries on AniList

    Returns:
        int: Total number of anime entries in AniList
    """
    api_url, headers = await _get_api_endpoint()
    query = await _load_graphql_query('get_anilist_total_anime.graphql')

    # --- http request to anilist api ---
    async with aiohttp_client.session.post(api_url, json={'query': query}, headers=headers) as resp:
        data = await resp.json()
        total_anime = data['data']['Page']['pageInfo']['total']

        return total_anime


async def fetch_random_anime() -> dict:
    """
    Fetch a random anime from AniList

    Returns:
        dict: Random anime entry
    """
    api_url, headers = await _get_api_endpoint()
    query = await _load_graphql_query('get_anilist_random_page.graphql')

    # --- Get anilist total animes ---
    total = await _get_al_animes()

    # Get random page, because anilist's api works by pagination, not index
    per_page = 25
    max_pages = (total // per_page) + 1
    random_page = random.randint(1, max_pages)

    # --- http request to anilist api ---
    json_query = {'query': query, 'variables': {'page': random_page, 'perPage': per_page}}
    async with aiohttp_client.session.post(api_url, json=json_query, headers=headers) as resp:
        data = await resp.json()
        random_anime = random.choice(data['data']['Page']['media'])

        return random_anime
