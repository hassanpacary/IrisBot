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

from bot.utils.strings_utils import get_string_segment


# ██████╗ ███████╗███████╗██████╗  ██████╗ ███╗   ██╗███████╗███████╗     ██████╗ ██████╗ ███╗   ██╗███████╗████████╗██████╗ ██╗   ██╗ ██████╗████████╗ ██████╗ ██████╗
# ██╔══██╗██╔════╝██╔════╝██╔══██╗██╔═══██╗████╗  ██║██╔════╝██╔════╝    ██╔════╝██╔═══██╗████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║   ██║██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
# ██████╔╝█████╗  ███████╗██████╔╝██║   ██║██╔██╗ ██║███████╗█████╗      ██║     ██║   ██║██╔██╗ ██║███████╗   ██║   ██████╔╝██║   ██║██║        ██║   ██║   ██║██████╔╝
# ██╔══██╗██╔══╝  ╚════██║██╔═══╝ ██║   ██║██║╚██╗██║╚════██║██╔══╝      ██║     ██║   ██║██║╚██╗██║╚════██║   ██║   ██╔══██╗██║   ██║██║        ██║   ██║   ██║██╔══██╗
# ██║  ██║███████╗███████║██║     ╚██████╔╝██║ ╚████║███████║███████╗    ╚██████╗╚██████╔╝██║ ╚████║███████║   ██║   ██║  ██║╚██████╔╝╚██████╗   ██║   ╚██████╔╝██║  ██║
# ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚══════╝     ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝  ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝


async def send_response_to_discord(
        target: discord.Interaction | discord.Message,
        content: str = None,
        files: list[discord.File] = None,
        embed: discord.Embed = None,
        ephemeral: bool = False,
        detach: bool = False,
):
    """
    Send a response to either a Discord Message or an Interaction

    Parameters:
        target (discord.Message | Interaction): The message or interaction to respond to
        content (str): The message text (optional)
        files (list[discord.File]): The files to send
        embed (discord.Embed): The embed to send
        ephemeral (bool): Whether the response should be ephemeral (only works with interactions)
        detach (bool): Whether the response should be detached (only works with interactions)
    """
    if files is None:
        files = []

    print(target.guild)
    # --- Response to Slash command ---
    if isinstance(target, discord.Interaction):

        # If flag detach is true, send a simple message in the channel
        if detach:
            await target.channel.send(content=content, files=files, embed=embed)

        # 2nd and all new response in the ctx
        elif target.response.is_done():  # type: ignore
            await target.followup.send(content=content, files=files, embed=embed, ephemeral=ephemeral)

        # 1st response
        else:
            await target.response.send_message(content=content, files=files, embed=embed, ephemeral=ephemeral)  # type: ignore

    # --- Response to user message ---
    elif isinstance(target, discord.Message):
        await target.channel.send(content=content, files=files, embed=embed)

    logging.info(f"-- Discord message has been sent: {content}")


# ███████╗███╗   ███╗██████╗ ███████╗██████╗      ██████╗██████╗ ███████╗ █████╗ ████████╗ ██████╗ ██████╗
# ██╔════╝████╗ ████║██╔══██╗██╔════╝██╔══██╗    ██╔════╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
# █████╗  ██╔████╔██║██████╔╝█████╗  ██║  ██║    ██║     ██████╔╝█████╗  ███████║   ██║   ██║   ██║██████╔╝
# ██╔══╝  ██║╚██╔╝██║██╔══██╗██╔══╝  ██║  ██║    ██║     ██╔══██╗██╔══╝  ██╔══██║   ██║   ██║   ██║██╔══██╗
# ███████╗██║ ╚═╝ ██║██████╔╝███████╗██████╔╝    ╚██████╗██║  ██║███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║
# ╚══════╝╚═╝     ╚═╝╚═════╝ ╚══════╝╚═════╝      ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝


async def create_discord_embed(
        color: discord.Color = discord.Color.blurple(),
        title: str = None,
        title_url: str = None,
        description: str = None,
        date: datetime = None,
        author: str = None,
        icon: str = None,
        fields: list[tuple] = None,
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
        fields (list[dict]): List of fields, each dict with 'name', 'value', 'inline' (optional, default True)
        thumbnail_url (str): URL for the embed thumbnail
        image_url (str): URL for the embed main image
        footer_text (str): Footer text
        footer_icon_url (str): Footer icon URL

    Returns:
        discord.Embed: The embed object
    """
    embed = discord.Embed(color=color, title=title, url=title_url, description=description, timestamp=date)
    embed.set_author(name=author, icon_url=icon)

    # Add fields if any
    if fields:
        for field_name, field_value in fields:
            embed.add_field(
                name=field_name,
                value=field_value,
                inline=True
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
        return discord.File(filename, filename=get_string_segment(string=filename, split_char="/", i=3))

    else:
        return discord.File(io.BytesIO(data), filename=filename)
