"""
anilist_service.py
© by hassanpacary

Service for fetching data from AniList API.
"""

# --- Imports ---
import random
import os

# --- Bot modules ---
from bot.utils.aiohttp_client import aiohttp_client
from bot.utils.files_utils import load_file, load_yaml


#  █████╗ ███╗   ██╗██╗██╗     ██╗███████╗████████╗    ███████╗███████╗██████╗ ██╗   ██╗██╗ ██████╗███████╗
# ██╔══██╗████╗  ██║██║██║     ██║██╔════╝╚══██╔══╝    ██╔════╝██╔════╝██╔══██╗██║   ██║██║██╔════╝██╔════╝
# ███████║██╔██╗ ██║██║██║     ██║███████╗   ██║       ███████╗█████╗  ██████╔╝██║   ██║██║██║     █████╗
# ██╔══██║██║╚██╗██║██║██║     ██║╚════██║   ██║       ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██║██║     ██╔══╝
# ██║  ██║██║ ╚████║██║███████╗██║███████║   ██║       ███████║███████╗██║  ██║ ╚████╔╝ ██║╚██████╗███████╗
# ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚══════╝╚═╝╚══════╝   ╚═╝       ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚═╝ ╚═════╝╚══════╝


async def load_api_endpoint() -> tuple[str, dict]:
    """
    Loads the GraphQL endpoint URL and headers from graphql.config.yml.

    Returns:
        tuple: (url: str, headers: dict)
    """
    graphql_config_path = os.path.join('bot', 'queries', 'graphql.config.yml')

    api_config = load_yaml(graphql_config_path)
    endpoint = api_config['extensions']['endpoints']['anilist']

    return endpoint['url'], endpoint.get('headers', {})


async def load_graphql_query(query: str) -> str:
    """Load a GraphQL query file from the queries/ directory."""
    query_file_path = os.path.join('bot', 'queries', query)

    # --- Read the query file ---
    return load_file(query_file_path, "r")


# ██████╗ ███████╗ ██████╗ ██╗   ██╗███████╗███████╗████████╗███████╗
# ██╔══██╗██╔════╝██╔═══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝██╔════╝
# ██████╔╝█████╗  ██║   ██║██║   ██║█████╗  ███████╗   ██║   ███████╗
# ██╔══██╗██╔══╝  ██║▄▄ ██║██║   ██║██╔══╝  ╚════██║   ██║   ╚════██║
# ██║  ██║███████╗╚██████╔╝╚██████╔╝███████╗███████║   ██║   ███████║
# ╚═╝  ╚═╝╚══════╝ ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝   ╚══════╝


async def get_anilist_total_anime() -> int:
    """Fetch the total number of anime entries on AniList."""
    api_url, headers = await load_api_endpoint()
    query = await load_graphql_query('get_anilist_total_anime.graphql')

    # --- http request to anilist api ---
    async with aiohttp_client.session.post(api_url, json={'query': query}, headers=headers) as resp:
        data = await resp.json()
        return data['data']['Page']['pageInfo']['total']


async def fetch_random_anime() -> dict:
    """Fetch a random anime from AniList."""
    api_url, headers = await load_api_endpoint()
    query = await load_graphql_query('get_anilist_random_page.graphql')

    # --- Get anilist total animes ---
    total = await get_anilist_total_anime()

    # Get random page, because anilist's api works by pagination, not index
    per_page = 25
    max_pages = (total // per_page) + 1
    random_page = random.randint(1, max_pages)

    # --- http request to anilist api ---
    json_query = {'query': query, 'variables': {'page': random_page, 'perPage': per_page}}
    async with aiohttp_client.session.post(api_url, json=json_query, headers=headers) as resp:
        data = await resp.json()
        return random.choice(data['data']['Page']['media'])
