"""
bot/utils/discord_utils.py
© by hassanpacary

Utility functions for discord.
"""

# --- Imports ---
from datetime import datetime
import io
import logging

# --- Third party imports ---
import discord

# --- Bot modules
from bot.utils.strings_utils import get_string_segment


# pylint: disable=line-too-long
# ██████╗ ███████╗███████╗██████╗  ██████╗ ███╗   ██╗███████╗███████╗     ██████╗ ██████╗ ███╗   ██╗███████╗████████╗██████╗ ██╗   ██╗ ██████╗████████╗ ██████╗ ██████╗
# ██╔══██╗██╔════╝██╔════╝██╔══██╗██╔═══██╗████╗  ██║██╔════╝██╔════╝    ██╔════╝██╔═══██╗████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║   ██║██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
# ██████╔╝█████╗  ███████╗██████╔╝██║   ██║██╔██╗ ██║███████╗█████╗      ██║     ██║   ██║██╔██╗ ██║███████╗   ██║   ██████╔╝██║   ██║██║        ██║   ██║   ██║██████╔╝
# ██╔══██╗██╔══╝  ╚════██║██╔═══╝ ██║   ██║██║╚██╗██║╚════██║██╔══╝      ██║     ██║   ██║██║╚██╗██║╚════██║   ██║   ██╔══██╗██║   ██║██║        ██║   ██║   ██║██╔══██╗
# ██║  ██║███████╗███████║██║     ╚██████╔╝██║ ╚████║███████║███████╗    ╚██████╗╚██████╔╝██║ ╚████║███████║   ██║   ██║  ██║╚██████╔╝╚██████╗   ██║   ╚██████╔╝██║  ██║
# ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚══════╝     ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝  ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
# pylint: enable=line-too-long


async def send_response_to_discord( # pylint: disable=too-many-arguments
        *,
        ctx: discord.Interaction | discord.Message,
        content: str = None,
        files: list[discord.File] = None,
        embed: discord.Embed = None,
        view: discord.ui.View = None,
        ephemeral: bool = False,
        detach: bool = False
):
    """
    Send a response to either a Discord Message or an Interaction

    Parameters:
        ctx (discord.Message | Interaction): The message or interaction to respond to
        content (str): The message text (optional)
        files (list[discord.File]): The files to send
        embed (discord.Embed): The embed to send
        view (discord.View): The view to use
        ephemeral (bool): Whether the response should be ephemeral (only works with interactions)
        detach (bool): Whether the response should be detached (only works with interactions)
    """
    if files is None:
        files = []

    # --- Response to Slash command ---
    if isinstance(ctx, discord.Interaction):

        # If flag detach is true, send a simple message in the channel
        if detach:
            await ctx.channel.send(content=content, files=files, embed=embed, view=view)

        # 2nd and all new response in the ctx
        elif ctx.response.is_done():  # type: ignore
            await ctx.followup.send(content=content, files=files, embed=embed, view=view, ephemeral=ephemeral)

        # 1st response
        else:
            await ctx.response.send_message( # type: ignore
                content=content,
                files=files,
                embed=embed,
                view=view,
                ephemeral=ephemeral
            )

    # --- Response to user message ---
    elif isinstance(ctx, discord.Message):
        await ctx.channel.send(content=content, files=files, embed=embed, view=view)

    logging.info(
        "-- Discord message has been sent: %s",
        content
    )


async def send_message_in_channel(
        ctx: discord.Member | discord.Message,
        channel_id: int = None,
        content: str = None,
        embed: discord.Embed = None,
):
    """
        Send a message in a specific channel or system channel

        Parameters:
            ctx (discord.Message | Interaction): The message or interaction to respond to
            channel_id (int): The channel to send to
            content (str): The message text (optional)
            embed (discord.Embed): The embed to send (optional)
        """

    # If a channel of message has been set up, we use this one
    if channel_id:
        system_channel_id = channel_id
    else:
        system_channel_id = ctx.guild.system_channel.id

    channel = await ctx.guild.fetch_channel(system_channel_id)
    await channel.send(content=content, embed=embed)


# pylint: disable=line-too-long
# ███████╗███╗   ███╗██████╗ ███████╗██████╗      ██████╗██████╗ ███████╗ █████╗ ████████╗ ██████╗ ██████╗
# ██╔════╝████╗ ████║██╔══██╗██╔════╝██╔══██╗    ██╔════╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
# █████╗  ██╔████╔██║██████╔╝█████╗  ██║  ██║    ██║     ██████╔╝█████╗  ███████║   ██║   ██║   ██║██████╔╝
# ██╔══╝  ██║╚██╔╝██║██╔══██╗██╔══╝  ██║  ██║    ██║     ██╔══██╗██╔══╝  ██╔══██║   ██║   ██║   ██║██╔══██╗
# ███████╗██║ ╚═╝ ██║██████╔╝███████╗██████╔╝    ╚██████╗██║  ██║███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║
# ╚══════╝╚═╝     ╚═╝╚═════╝ ╚══════╝╚═════╝      ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
# pylint: enable=line-too-long


async def create_discord_embed( # pylint: disable=too-many-arguments
        *,
        color: discord.Color = discord.Color.blurple(),
        title: str = None,
        title_url: str = None,
        description: str = None,
        date: datetime = None,
        author: str = None,
        icon: str = None,
        fields: list[tuple] = None,
        fields_is_inline: bool = True,
        thumbnail_url: str = None,
        image_url: str = None,
        footer_text: str = None,
        footer_icon_url: str = None
) -> discord.Embed:
    """
    Sends a Discord embed to either an Interaction or a Message

    Parameters:
        color (discord.Color): Embed color
        title (str): Embed title
        title_url (str): Embed title URL
        description (str): Embed description
        date (datetime | None): Embed date
        author (str): Embed author
        icon (str): Embed icon
        fields (list[dict]):
                List of fields, each dict with 'name', 'value', 'inline' (optional, default True)
        fields_is_inline (bool): Whether the fields should be inline
        thumbnail_url (str): URL for the embed thumbnail
        image_url (str): URL for the embed main image
        footer_text (str): Footer text
        footer_icon_url (str): Footer icon URL

    Returns:
        discord.Embed: The embed object
    """
    embed = discord.Embed(
        color=color,
        title=title,
        url=title_url,
        description=description,
        timestamp=date
    )
    embed.set_author(name=author, icon_url=icon)

    # Add fields if any
    if fields:
        for field_name, field_value in fields:
            embed.add_field(
                name=field_name,
                value=field_value,
                inline=fields_is_inline
            )

    # Add thumbnail and image
    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)
    if image_url:
        embed.set_image(url=image_url)

    # Add footer
    if footer_text:
        embed.set_footer(text=footer_text, icon_url=footer_icon_url)

    return embed


#  ██████╗██████╗ ███████╗ █████╗ ████████╗███████╗    ███████╗██╗██╗     ███████╗
# ██╔════╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔════╝    ██╔════╝██║██║     ██╔════╝
# ██║     ██████╔╝█████╗  ███████║   ██║   █████╗      █████╗  ██║██║     █████╗
# ██║     ██╔══██╗██╔══╝  ██╔══██║   ██║   ██╔══╝      ██╔══╝  ██║██║     ██╔══╝
# ╚██████╗██║  ██║███████╗██║  ██║   ██║   ███████╗    ██║     ██║███████╗███████╗
#  ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝    ╚═╝     ╚═╝╚══════╝╚══════╝


async def create_discord_file(filename: str, data: bytes = None) -> discord.File:
    """
    Create a discord.File object from raw bytes

    Parameters:
        data (bytes): Raw file data
        filename (str): Filename to assign to the file

    Returns:
        discord.File: A Discord-compatible file object
    """
    if data is None:
        return discord.File(
            filename,
            filename=get_string_segment(string=filename, split_char="/", i=3)
        )

    return discord.File(io.BytesIO(data), filename=filename)
