"""IsThereAnyDeal (ITAD) API requests.

Fetches latest video game deals from the ITAD API and normalizes
the raw response into a flat list of deal dicts.

Also resolves the deals URL by following redirect chain to get the final URL
(url of the shop).

Used by deals service for notifies all member of the guild with the news discounts.

© by hassanpacary
"""

# --- Standard library ---
import logging

# --- Third_party
import aiohttp

# --- Internal ---
from bot.cogs.guild import guild_config
from bot.core import environment

# --- Constants ---
_ITAD_API_URL: str = "https://api.isthereanydeal.com/deals/v2"
_ITAD_HEADERS: dict = {"Content-Type": "application/json"}


async def _fetch_raw_deals() -> dict:
    """Fetches raw deals data from the ITAD API.

    Returns:
        The raw API response as a dict, or an empty dict on failure.
    """
    params = {
        "key": environment.get_env_var("ITAD_API_KEY"),
        "params": guild_config.Itad.PARAMS,
    }

    try:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(
                url=_ITAD_API_URL,
                headers=_ITAD_HEADERS,
                params=params,
            )
        return await resp.json()
    except aiohttp.ClientError as e:
        logging.error("Failed to fetch deals from ITAD: %s", e)
        return {}


async def _resolve_deal_url(url: str) -> str:
    """Resolves a deal URL by following redirects to get the final URL.

    Args:
        url: The raw deal URL to resolve.

    Returns:
        The final resolved URL as a string, or first url on failure.
    """
    try:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(url=url, allow_redirects=True)
        return str(resp.url)
    except aiohttp.ClientError as e:
        logging.warning("Failed to resolve URL %s: %s", url, e)
        return url


# --- Exposed functions ---


async def fetch_deals() -> list[dict]:
    """Fetches current deals from ITAD and normalizes them into a flat list.

    Calls the ITAD API with the configured filters and maps each raw
    deal entry into a normalized dict with consistent key names.

    The shop URL field call _resolve_deal_url for get the final redirect
    destination url, the direct shop URL and not the deal URL, to bypass trackers.

    Returns:
        A list of normalized deal dicts, or an empty list if the API returns no data.
    """

    data = await _fetch_raw_deals()

    return [
        {
            "id": deal["id"],
            "title": deal["title"],
            "type": deal["type"],
            "assets": deal["assets"],
            "deal": {
                "shop": _resolve_deal_url(deal["deal"]["shop"]),
                "new_price": deal["deal"]["price"]["amount"],
                "old_price": deal["deal"]["regular"]["amount"],
                "pourcent": deal["deal"]["cut"],
                "historyLow": deal["deal"]["storeLow"]["amount"],
                "limit_date": deal["deal"]["expiry"],
                "url": deal["deal"]["url"],
            },
        }
        for deal in data.get("list", [])
    ]
