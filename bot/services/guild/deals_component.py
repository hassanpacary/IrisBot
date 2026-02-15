"""
bot/services/guild/deals_component.py
© by hassanpacary

Utility functions to manage Discord bot videos games deals notifications
"""

# --- Imports ---
import os
from datetime import datetime

# --- Third party imports ---
import discord
from discord.ext import commands

# --- Bot modules ---
from bot.core.config_loader import BOT, STRINGS
from bot.services.guild.itad_api_service import fetch_deals_data
from bot.utils.discord_utils import send_message_in_channel, create_discord_embed
from bot.utils.files_utils import load_json, write_json


# pylint: disable=line-too-long
# ██████╗ ███████╗ █████╗ ██╗     ███████╗    ███╗   ██╗ ██████╗ ████████╗██╗███████╗██╗ ██████╗ █████╗ ████████╗██╗ ██████╗ ███╗   ██╗███████╗
# ██╔══██╗██╔════╝██╔══██╗██║     ██╔════╝    ████╗  ██║██╔═══██╗╚══██╔══╝██║██╔════╝██║██╔════╝██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝
# ██║  ██║█████╗  ███████║██║     ███████╗    ██╔██╗ ██║██║   ██║   ██║   ██║█████╗  ██║██║     ███████║   ██║   ██║██║   ██║██╔██╗ ██║███████╗
# ██║  ██║██╔══╝  ██╔══██║██║     ╚════██║    ██║╚██╗██║██║   ██║   ██║   ██║██╔══╝  ██║██║     ██╔══██║   ██║   ██║██║   ██║██║╚██╗██║╚════██║
# ██████╔╝███████╗██║  ██║███████╗███████║    ██║ ╚████║╚██████╔╝   ██║   ██║██║     ██║╚██████╗██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║███████║
# ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝    ╚═╝  ╚═══╝ ╚═════╝    ╚═╝   ╚═╝╚═╝     ╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
# pylint: enable=line-too-long


async def _notif_deal(ctx: commands.Bot, deal: dict):
    """
    Send a notification in a Discord channel with deal information

    Parameters:
        ctx (commands.Context): discord context
        deal (dict): deal information
    """
    color = BOT['color']['deals']
    deals_chan_id = BOT['channels']['deals']

    date = deal['deal']['limit_date']
    date_format = STRINGS['guild']['deals_component']['embed_description_field_date_data']
    if date is not None:
        date = datetime.fromisoformat(date)
        date_format = date.strftime("%d %b %Y à %H:%M")

    asset = None
    if deal['assets'] is not {}:
        if "banner600" in deal['assets'] :
            asset = deal['assets']['banner600']

    deal_embed = await create_discord_embed(
        color=discord.Color(int(color, 16)),
        title=deal['title'],
        title_url=deal['deal']['url'],
        description=STRINGS['guild']['deals_component']['embed_description_field'].format(
            pourcent=deal['deal']['pourcent'],
            date=date_format
        ),
        author=STRINGS['guild']['deals_component']['embed_author_field'].format(
            store=deal['deal']['shop']['name']
        ),
        fields=[
            (
                STRINGS['guild']['deals_component']['embed_new_price_field_label'],
                STRINGS['guild']['deals_component']['embed_new_price_field'].format(
                    new_price=deal['deal']['new_price'])
            ),
            (
                STRINGS['guild']['deals_component']['embed_old_price_field_label'],
                STRINGS['guild']['deals_component']['embed_old_price_field'].format(
                    old_price=deal['deal']['old_price'])
            ),
            (
                STRINGS['guild']['deals_component']['embed_history_low_field_label'],
                STRINGS['guild']['deals_component']['embed_history_low_field'].format(
                    history_price=deal['deal']['historyLow'])
            ),
        ],
        thumbnail_url=str(BOT['deals'][str(deal['deal']['shop']['id'])]),
        image_url=asset
    )

    await send_message_in_channel(ctx=ctx, channel_id=deals_chan_id, embed=deal_embed)

async def check_deals(ctx: commands.Bot):
    """Logic to check the deals api (itad) for new deals"""
    json_path = os.path.join("bot", "data", "deals_list.json")
    old_deals_id = load_json(json_path)

    new_deals = await fetch_deals_data()
    new_deals_id = [deal["id"] for deal in new_deals]

    for deal in new_deals:
        if deal['id'] not in old_deals_id:
            await _notif_deal(ctx=ctx, deal=deal)

    write_json(file_path=json_path, data=new_deals_id)