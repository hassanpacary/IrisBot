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
        ephemeral: bool = False
) -> None:
    """
    Send a response to either a Discord Message or an Interaction.

    Args:
        target (discord.Message | Interaction): The message or interaction to respond to.
        content (str): The message text (optional).
        files (list[discord.File]): The files to send.
        embed (discord.Embed): The embed to send.
        ephemeral (bool): Whether the response should be ephemeral (only works with interactions).
    """
    if files is None:
        files = []

    # --- Response to Slash command ---
    if isinstance(target, discord.Interaction):
        if target.response.is_done():  # type: ignore
            await target.followup.send(content=content, files=files, embed=embed, ephemeral=ephemeral)
        else:
            await target.response.send_message(content=content, files=files, embed=embed, ephemeral=ephemeral)  # type: ignore

    # --- Response to user message ---
    elif isinstance(target, discord.Message):
        await target.reply(content=content, files=files, embed=embed)

    logging.info(f"-- Discord message has been sent: {content} with files: {files}")


# ███████╗███╗   ███╗██████╗ ███████╗██████╗      ██████╗██████╗ ███████╗ █████╗ ████████╗ ██████╗ ██████╗
# ██╔════╝████╗ ████║██╔══██╗██╔════╝██╔══██╗    ██╔════╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
# █████╗  ██╔████╔██║██████╔╝█████╗  ██║  ██║    ██║     ██████╔╝█████╗  ███████║   ██║   ██║   ██║██████╔╝
# ██╔══╝  ██║╚██╔╝██║██╔══██╗██╔══╝  ██║  ██║    ██║     ██╔══██╗██╔══╝  ██╔══██║   ██║   ██║   ██║██╔══██╗
# ███████╗██║ ╚═╝ ██║██████╔╝███████╗██████╔╝    ╚██████╗██║  ██║███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║
# ╚══════╝╚═╝     ╚═╝╚═════╝ ╚══════╝╚═════╝      ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝


async def send_embed_to_discord(
        target: discord.Interaction | discord.Message,
        color: discord.Color = discord.Color.blurple(),
        title: str = None,
        title_url: str = None,
        description: str = None,
        date: datetime | None = None,
        author: str = None,
        icon: str = None,
        fields: list[dict] = None,
        thumbnail_url: str = None,
        image_url: str = None,
        footer_text: str = None,
        footer_icon_url: str = None
) -> None:
    """
    Sends a Discord embed to either an Interaction or a Message.

    Args:
        target (discord.Interaction | discord.Message): Target to send the embed to.
        color (discord.Color): Embed color.
        title (str): Embed title.
        title_url (str): Embed title URL.
        description (str): Embed description.
        date (datetime | None): Embed date.
        author (str): Embed author.
        icon (str): Embed icon.
        fields (list[dict]): List of fields, each dict with 'name', 'value', 'inline' (optional, default True).
        thumbnail_url (str): URL for the embed thumbnail.
        image_url (str): URL for the embed main image.
        footer_text (str): Footer text.
        footer_icon_url (str): Footer icon URL.
    """
    embed = discord.Embed(color=color, title=title, url=title_url, description=description, timestamp=date)
    embed.set_author(name=author, icon_url=icon)

    # Add fields if any
    if fields:
        for field in fields:
            embed.add_field(
                name=field.get("name", "Unnamed"),
                value=field.get("value", "\u200b"),
                inline=field.get("inline", True)
            )

    # Add thumbnail and image
    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)
    if image_url:
        embed.set_image(url=image_url)

    # Add footer
    if footer_text:
        embed.set_footer(text=footer_text, icon_url=footer_icon_url)

    await send_response_to_discord(
        target=target,
        embed=embed
    )


#  ██████╗██████╗ ███████╗ █████╗ ████████╗███████╗    ███████╗██╗██╗     ███████╗
# ██╔════╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔════╝    ██╔════╝██║██║     ██╔════╝
# ██║     ██████╔╝█████╗  ███████║   ██║   █████╗      █████╗  ██║██║     █████╗
# ██║     ██╔══██╗██╔══╝  ██╔══██║   ██║   ██╔══╝      ██╔══╝  ██║██║     ██╔══╝
# ╚██████╗██║  ██║███████╗██║  ██║   ██║   ███████╗    ██║     ██║███████╗███████╗
#  ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝    ╚═╝     ╚═╝╚══════╝╚══════╝


def create_discord_file(data: bytes, filename: str) -> discord.File:
    """
    Create a discord.File object from raw bytes.

    Args:
        data (bytes): Raw file data.
        filename (str): Filename to assign to the file.

    Returns:
        discord.File: A Discord-compatible file object.
    """
    return discord.File(io.BytesIO(data), filename=filename)
