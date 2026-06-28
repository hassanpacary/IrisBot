"""Quote fest service for fun cog.

Manage logics functions for ending the quote festival task
(reset quote channel and announcement of the month winners).

© by hassanpacary
"""

# --- Forward references ---
from __future__ import annotations

# --- Standard library ---
from datetime import datetime, timezone
from typing import TYPE_CHECKING

# --- Third-party ---
import discord
from dateutil.relativedelta import relativedelta

# --- Internal ---
from bot.cogs.fun import fun_strings
from bot.config import assets_config, bot_config
from bot.utils import discord_utils

if TYPE_CHECKING:
    from bot.core import bot as b


async def _get_messages_of_month(channel: discord.TextChannel) -> list[discord.Message]:
    """Retrieves all messages posted in the fest channel during the last month.

    Args:
        channel: The Discord TextChannel to fetch history from.

    Returns:
        A list of discord.Message objects from the past month.
    """
    end_date = datetime.now(tz=timezone.utc)
    start_date = end_date - relativedelta(months=1)

    return [
        message
        async for message in channel.history(after=start_date, before=end_date)
    ]


async def _get_top_quoted_message(
        channel: discord.TextChannel,
) -> discord.Message:
    """Returns the most reacted message in the channel from the past month.

    Args:
        channel: The Discord TextChannel to search.

    Returns:
        The message with the highest total reaction count, or None if the
        channel has no messages from the past month.

    Raises:
        ValueError: If no quoted messages were found in the past month.
    """
    messages = await _get_messages_of_month(channel=channel)

    if not messages:
        raise ValueError("No quoted messages found for this month")

    return max(
        messages,
        key=lambda m: sum(reaction.count for reaction in m.reactions),
    )


async def announce_fest_winners(bot: b.Bot) -> None:
    """Announces the most quoted message of the month and resets the channel.

    Args:
        bot: The Discord bot instance.
    """
    channel = await discord_utils.get_channel_by_ctx(
        ctx=bot,
        channel_id=bot_config.ChannelsId.QUOTES,
    )

    top_message = await _get_top_quoted_message(channel)
    embed = top_message.embeds[0]
    ctx_user = embed.fields[0].value
    author_user = embed.fields[1].value

    splitter = discord.File(fp=assets_config.SPLITTER_PATH)

    await channel.send(file=splitter)
    result_message = await channel.send(
        content=fun_strings.Quote.MONTH_RESULT.format(
            month=datetime.now(tz=timezone.utc).strftime("%B"),
            discloser=ctx_user,
            author=author_user,
        )
    )
    await result_message.reply(embed=embed)
    await channel.send(file=splitter)
