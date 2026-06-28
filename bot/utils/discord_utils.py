"""Discord utilities functions.

Manage utilities functions for build a Discord embed, get bot icon and
get channel by is context.

© by hassanpacary
"""

# --- Standard library ---
from datetime import datetime
from typing import cast

# --- Third-party ---
import discord
from discord.ext import commands
from discord.utils import MISSING


async def create_discord_embed(  # pylint: disable=too-many-arguments, too-many-locals
    *,
    color: discord.Color = discord.Color.blurple(),
    title: str = MISSING,
    title_url: str = MISSING,
    description: str = MISSING,
    date: datetime | None = None,
    author: str = MISSING,
    icon: str = MISSING,
    fields: list[tuple[str, str]] = MISSING,
    fields_is_inline: bool = True,
    thumbnail_url: str = MISSING,
    image_url: str | None = None,
    footer_text: str = MISSING,
    footer_icon_url: str = MISSING,
) -> discord.Embed:
    """Builds a Discord embed from the provided parameters.

    Args:
        color: Embed color. Defaults to blurple.
        title: Embed title.
        title_url: URL linked from the title.
        description: Embed description text.
        date: Timestamp shown in the footer. Defaults to now.
        author: Author name shown at the top.
        icon: Author icon URL.
        fields: List of (name, value) tuples to add as fields.
        fields_is_inline: Whether fields are displayed inline.
            Defaults to True.
        thumbnail_url: URL of the thumbnail image.
        image_url: URL of the main embed image.
        footer_text: Footer text.
        footer_icon_url: Footer icon URL.

    Returns:
        A fully constructed discord.Embed instance.
    """
    embed = discord.Embed(
        color=color,
        title=title if title is not MISSING else None,
        url=title_url if title_url is not MISSING else None,
        description=description if description is not MISSING else None,
        timestamp=date or datetime.now(),
    )

    if author is not MISSING:
        embed.set_author(
            name=author,
            icon_url=icon if icon is not MISSING else None,
        )

    if fields is not MISSING:
        for field_name, field_value in fields:
            embed.add_field(
                name=field_name,
                value=field_value,
                inline=fields_is_inline,
            )

    if thumbnail_url is not MISSING:
        embed.set_thumbnail(url=thumbnail_url)

    if image_url is not None:
        embed.set_image(url=image_url)

    if footer_text is not MISSING:
        embed.set_footer(
            text=footer_text,
            icon_url=footer_icon_url if footer_icon_url is not MISSING else None,
        )

    return embed


def get_bot_icon(bot: commands.Bot) -> str:
    """Returns the bot's avatar URL, or MISSING if unavailable.

    Args:
        bot: The Discord bot instance.

    Returns:
        The bot avatar URL as a string, or MISSING.
    """
    bot_user = cast(discord.ClientUser, bot.user)
    avatar = getattr(bot_user, "avatar", None)
    return str(getattr(avatar, "url", MISSING)) if avatar else MISSING


async def get_channel_by_ctx(
    ctx: commands.Bot | discord.Message | discord.Interaction,
    channel_id: int,
) -> discord.TextChannel:
    """Get the target channel from the guild, depending on the type of ctx provided.

    Args:
        ctx: The bot instance, a guild member, or a message.
        channel_id: The ID of the channel to send the message to.

    Raise:
        ValueError: If the channel is impossible to retrieve.
    """
    if isinstance(ctx, commands.Bot):
        channel = cast(discord.TextChannel, await ctx.fetch_channel(channel_id))
    elif ctx.guild is not None:
        guild = cast(discord.Guild, ctx.guild)
        channel = cast(discord.TextChannel, await guild.fetch_channel(channel_id))
    else:
        raise ValueError(
            f"Impossible to retrieve the discord TextChannel {channel_id}",
        )

    return channel


def get_guild_icon(
        bot: commands.Bot | None = None,
        guild: discord.Guild | None = None,
) -> str:
    """Returns the guild icon URL, or MISSING if unavailable.

    Args:
        bot: The Discord bot instance.
        guild: The Discord guild instance.

    Returns:
        The guild icon URL as a string, or MISSING.
    """
    if bot is not None:
        guild = bot.guilds[0]
        icon = getattr(guild, "icon", None)
        return str(getattr(icon, "url", MISSING)) if icon else MISSING

    icon = getattr(guild, "icon", None)
    return str(getattr(icon, "url", MISSING)) if icon else MISSING
