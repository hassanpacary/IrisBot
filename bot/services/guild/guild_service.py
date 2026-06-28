"""Guild service for guild cog.

Manage logics functions for guild logging messages, welcome and goodbye messages.

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
from bot.config import bot_config, colors_config
from bot.cogs.core import core_strings
from bot.cogs.guild import guild_strings
from bot.utils import discord_utils

if TYPE_CHECKING:
    from bot.core import bot as b


async def log_deleted_message(
        bot: b.Bot,
        message: discord.Message,
) -> None:
    """Logs a deleted message as an embed in the log channel.

    Args:
        bot: The Discord bot instance.
        message: The deleted Discord message.
    """
    icon = discord_utils.get_guild_icon(bot=bot, guild=None)

    embed = await discord_utils.create_discord_embed(
        color=discord.Color(int(colors_config.RED, 16)),
        title=message.author.name,
        description=message.content,
        date=message.created_at,
        author=guild_strings.Logs.DELETED_MESSAGE,
        icon=icon,
        thumbnail_url=str(message.author.display_avatar.url),
        footer_text=core_strings.GUILD_NAME,
    )

    channel = await discord_utils.get_channel_by_ctx(
        ctx=bot,
        channel_id=bot_config.ChannelsId.LOGS,
    )
    await channel.send(embed=embed)


async def log_edited_message(
        bot: b.Bot,
        message_before: discord.Message,
        message_after: discord.Message,
) -> None:
    """Logs an edited message as an embed in the log channel.

    Args:
        bot: The Discord bot instance.
        message_before: The message content before the edit.
        message_after: The message content after the edit.
    """
    icon = discord_utils.get_guild_icon(bot=bot, guild=None)

    embed = await discord_utils.create_discord_embed(
        color=discord.Color(int(colors_config.RED, 16)),
        title=message_before.author.name,
        description=message_before.content,
        date=message_before.created_at,
        author=guild_strings.Logs.EDITED_MESSAGE,
        icon=icon,
        fields=[
            (guild_strings.Logs.NEW_MESSAGE_FIELD, message_after.content),
        ],
        thumbnail_url=str(message_before.author.display_avatar.url),
        footer_text=core_strings.GUILD_NAME,
    )

    channel = await discord_utils.get_channel_by_ctx(
        ctx=bot,
        channel_id=bot_config.ChannelsId.LOGS,
    )
    await channel.send(embed=embed)


async def welcome(bot: b.Bot, user: discord.User) -> None:
    """Sends a random welcome message when a new user joins the server.

    Args:
        bot: The Discord bot instance.
        user: The Discord user who joined the guild.
    """
    channel = await discord_utils.get_channel_by_ctx(
        ctx=bot,
        channel_id=bot_config.ChannelsId.WELCOME,
    )
    await channel.send(
        content=random.choice(guild_strings.WELCOME_MESSAGES).format(user=user.mention),
    )


async def goodbye(bot: b.Bot, user: discord.User) -> None:
    """Sends a random goodbye message when a user leaves the server.

    Args:
        bot: The Discord bot instance.
        user: The Discord user who left the guild.
    """
    channel = await discord_utils.get_channel_by_ctx(
        ctx=bot,
        channel_id=bot_config.ChannelsId.GOODBYE,
    )
    await channel.send(
        content=random.choice(guild_strings.GOODBYE_MESSAGES).format(user=user.mention),
    )
