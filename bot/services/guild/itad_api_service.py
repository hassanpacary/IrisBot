"""
bot/services/guild/itad_api_service.py
© by hassanpacary

Utility functions for checked IsThereAnyDeal API for videos games deals
"""

# --- Imports ---
import os

# --- Bot modules ---
from bot.core.config_loader import BOT
from bot.utils.aiohttp_client import aiohttp_client


# ██╗████████╗ █████╗ ██████╗     ███████╗███████╗██████╗ ██╗   ██╗██╗ ██████╗███████╗
# ██║╚══██╔══╝██╔══██╗██╔══██╗    ██╔════╝██╔════╝██╔══██╗██║   ██║██║██╔════╝██╔════╝
# ██║   ██║   ███████║██║  ██║    ███████╗█████╗  ██████╔╝██║   ██║██║██║     █████╗
# ██║   ██║   ██╔══██║██║  ██║    ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██║██║     ██╔══╝
# ██║   ██║   ██║  ██║██████╔╝    ███████║███████╗██║  ██║ ╚████╔╝ ██║╚██████╗███████╗
# ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═════╝     ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚═╝ ╚═════╝╚══════╝


async def _get_itad_data() -> dict:
    """
    Get the all current deals of videos games entries on ITAD

    Returns:
        dict: all deals data
    """
    api_url = os.environ['ITAD_API_URL']
    api_headers = {"Content-Type": "application/json"}

    params = {"key": os.environ['ITAD_API_KEY']} | BOT['deals']['params']

    # --- http request to ITAD api ---
    data = {}
    async with aiohttp_client.session.get(url=api_url, params=params, headers=api_headers) as resp:
        data = await resp.json()

    return data


async def fetch_deals_data() -> list:
    """
    Fetch desired data

    Returns:
        list: desired data from all deals data
    """
    deals = []

    data = await _get_itad_data()

    if data == {}:
        return []

    deals = [
        {
            "id": deal['id'],
            "title": deal['title'],
            "type": deal['type'],
            "assets": deal['assets'],
            "deal": {
                "shop": deal['deal']['shop'],
                "new_price": deal['deal']['price']['amount'],
                "old_price": deal['deal']['regular']['amount'],
                "pourcent": deal['deal']['cut'],
                "historyLow": deal['deal']['storeLow']['amount'],
                "limit_date": deal['deal']['expiry'],
                "url": deal['deal']['url']
            }
        }
        for deal in data['list']
    ]

    return deals
