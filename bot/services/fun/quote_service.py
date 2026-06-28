"""Quote service for fun cog.

Manage logics functions for quote command (by screenshot),
quote context command (by context), quote reaction (by reaction).

© by hassanpacary
"""

# --- Forward references ---
from __future__ import annotations

# --- Standard library ---
import logging
from datetime import datetime
from typing import TYPE_CHECKING

# --- Third-party ---
import discord
from discord.utils import MISSING

# --- Internal ---
from bot.cogs.fun import fun_strings
from bot.config import bot_config, colors_config
from bot.utils import discord_utils

if TYPE_CHECKING:
    from bot.core import bot as b


async def _build_message_embed(
        quoted_user: discord.User | discord.Member,
        message_content: str,
        date: datetime,
        ctx_user: discord.User | discord.Member
) -> discord.Embed:
    """Builds a quote embed for send it in quote channel.

    Args:
        quoted_user: The user who was quoted.
        message_content: The quoted message content (by context and reaction).
        date: The date the quoted message was sent.
        ctx_user: The user who trigger the command.

    Returns:
        A fully constructed discord.Embed instance.
    """
    return await discord_utils.create_discord_embed(
        color=discord.Color(int(colors_config.YELLOW, 16)),
        title=quoted_user.display_name,
        description=fun_strings.Quote.START_QUOTE
        + message_content
        + fun_strings.Quote.END_QUOTE,
        date=date,
        author=fun_strings.Quote.DISCLOSER_MEMBER.format(
            user=ctx_user.display_name,
        ),
        icon=str(getattr(ctx_user.avatar, "url", MISSING)),
        fields=[
            (fun_strings.Quote.DISCLOSER_MEMBER, ctx_user.mention),
            (fun_strings.Quote.QUOTED_USER, quoted_user.mention)
        ],
        footer_text=fun_strings.Quote.FOOTER,
    )


async def quote_user_by_context(
        interaction: discord.Interaction,
        message: discord.Message,
) -> None:
    """Quotes a message via the right-click context menu.

    Args:
        interaction: The Discord interaction context.
        message: The target message to quote.
    """
    channel = await discord_utils.get_channel_by_ctx(
        ctx=interaction,
        channel_id=bot_config.ChannelsId.QUOTES,
    )

    embed = await _build_message_embed(
        quoted_user=message.author,
        message_content=message.content,
        date=message.created_at,
        ctx_user=interaction.user,
    )

    await channel.send(embed=embed)
    await interaction.response.send_message(
        content=fun_strings.Quote.HANDLE_QUOTE_RESPONSE,
    )

    logging.info(
        "%s quoted a message from %s via context menu.",
        interaction.user.name,
        message.author.name,
    )


async def quote_user_by_screenshot(
        interaction: discord.Interaction,
        screen: discord.Attachment,
) -> None:
    """Quotes a message via a screenshot attachment.

    Args:
        interaction: The Discord interaction context.
        screen: The screenshot attachment to quote.
    """
    channel = await discord_utils.get_channel_by_ctx(
        ctx=interaction,
        channel_id=bot_config.ChannelsId.QUOTES,
    )

    embed = await discord_utils.create_discord_embed(
        color=discord.Color(int(colors_config.YELLOW, 16)),
        author=fun_strings.Quote.DISCLOSER_MEMBER.format(
            user=interaction.user.display_name,
        ),
        icon=str(getattr(interaction.user.avatar, "url", MISSING)),
        image_url=screen.url,
        footer_text=fun_strings.Quote.FOOTER,
    )

    await channel.send(embed=embed)
    await interaction.response.send_message(fun_strings.Quote.HANDLE_QUOTE_RESPONSE)

    logging.info(
        "%s quoted a message via screenshot.",
        interaction.user.name,
    )


async def quote_user_by_reaction(
        bot: b.Bot,
        payload: discord.RawReactionActionEvent,
) -> None:
    """Quotes a message by configured reaction emoji is added at message.

    Args:
        bot: The Discord bot instance.
        payload: The raw reaction event payload.

    Raises:
        ValueError: If no member who react to the post was found.
    """
    message_channel = await discord_utils.get_channel_by_ctx(
        ctx=bot,
        channel_id=payload.channel_id,
    )
    message = await message_channel.fetch_message(payload.message_id)
    quote_channel = await discord_utils.get_channel_by_ctx(
        ctx=bot,
        channel_id=bot_config.ChannelsId.QUOTES,
    )

    member = payload.member
    if member is None:
        raise ValueError(
            f"Guild member {payload.member} who react to the post is None.",
        )

    embed = await _build_message_embed(
        quoted_user=message.author,
        message_content=message.content,
        date=message.created_at,
        ctx_user=payload.member,
    )

    await quote_channel.send(embed=embed)
    await message_channel.send(content=fun_strings.Quote.HANDLE_QUOTE_RESPONSE)

    logging.info(
        "%s quoted a message from %s via reaction",
        payload.member.name,
        message.author.name,
    )
