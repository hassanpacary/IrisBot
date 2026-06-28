"""Deals service for fun cog.

Manage logics functions for videos games deals notifications task.
Fetches new deals from ITAD, compares them against the last known
deals list, and sends Discord notifications for any new entries.

© by hassanpacary
"""

# --- Forward references ---
from __future__ import annotations

# --- Standard library ---
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

# --- Third-party ---
import discord
from discord import TextChannel

# --- Internal ---
from bot.api.is_there_any_deals import itad_api_requests
from bot.cogs.guild import guild_config, guild_strings
from bot.config import colors_config, bot_config
from bot.utils import discord_utils, files_utils

if TYPE_CHECKING:
    from bot.core import bot as b

# --- Constants ---
_DEALS_LIST_PATH: Path = Path("bot") / "data" / "deals_list.json"


async def _build_deal_embed(deal: dict) -> discord.Embed:
    """Builds a Discord embed for a single deal notification.

    Args:
        deal: A deal dict as returned by fetch_deals_data().

    Returns:
        A fully constructed discord.Embed instance.
    """
    date = deal['deal']['limit_date']
    if date is not None:
        description = guild_strings.DealsEmbedFields.DESCRIPTION.format(
            pourcent=deal['deal']['pourcent'],
            date=datetime.fromisoformat(date).strftime("%d %b %Y à %H:%M")
        )
    else:
        description = guild_strings.DealsEmbedFields.DESCRIPTION_WITH_NO_DATE.format(
            pourcent=deal['deal']['pourcent'],
        )

    asset = None
    if deal['assets'] and "banner600" in deal['assets']:
        asset = str(deal['assets']['banner600'])

    return await discord_utils.create_discord_embed(
        color=discord.Color(int(colors_config.Utils.DEALS_EMBED, 16)),
        title=deal['title'],
        title_url=deal['deal']['url'],
        description=description,
        author=guild_strings.DealsEmbedFields.AUTHOR.format(
            store=deal['deal']['shop']['name'],
        ),
        fields=[
            (
                guild_strings.DealsEmbedFields.NEW_PRICE_LABEL,
                guild_strings.DealsEmbedFields.NEW_PRICE.format(
                    new_price=deal['deal']['new_price'],
                ),
            ),
            (
                guild_strings.DealsEmbedFields.OLD_PRICE_LABEL,
                guild_strings.DealsEmbedFields.OLD_PRICE.format(
                    new_price=deal['deal']['old_price'],
                ),
            ),
            (
                guild_strings.DealsEmbedFields.HISTORY_LOW_PRICE_LABEL,
                guild_strings.DealsEmbedFields.HISTORY_LOW_PRICE.format(
                    history_price=deal['deal']['historyLow'],
                ),
            ),
        ],
        thumbnail_url=str(
            guild_config.Itad.STORES_ICONS[
                str(deal['deal']['shop']['id']),
            ],
        ),
        image_url=asset,
    )


async def check_deals(bot: b.Bot) -> None:
    """Checks ITAD for new deals and notifies the deals channel.

    Compares newly fetched deals against the previously stored deal IDs.
    Sends a notification for each new deal and updates the stored list.

    Args:
        bot: The Discord bot instance.

    Raises:
        ValueError: If deals channel is not a TextChannel.
    """
    channel = discord_utils.get_channel_by_ctx(
        ctx=bot,
        channel_id=bot_config.ChannelsId.DEALS,
    )

    if not isinstance(channel, TextChannel):
        raise ValueError("Deals channel is not a TextChannel")

    old_deal_ids = await files_utils.load_json(fp=_DEALS_LIST_PATH)
    new_deals: list = await itad_api_requests.fetch_deals()

    for deal in new_deals:
        if deal['id'] not in old_deal_ids:
            embed = await _build_deal_embed(deal)
            await channel.send(embed=embed)

    await files_utils.write_json(fp=_DEALS_LIST_PATH, data=[d['id'] for d in new_deals])
