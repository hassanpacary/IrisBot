"""
bot/services/response_service.py
© by hassanpacary

Useful services for send response to discord user.
"""

# --- Imports ---
import io
import logging

# --- Third party imports ---
import discord

# --- Bot modules ---
from bot.core.config_loader import STRINGS, REGEX
from bot.services.reddit_service import fetch_reddit_medias
from bot.services.video_service import get_video
from bot.utils.aiohttp_client import aiohttp_client
from bot.utils.discord_utils import send_response_to_discord
from bot.utils.strings_utils import matches_pattern, get_string_segment


# ███████╗██╗██╗     ███████╗███████╗
# ██╔════╝██║██║     ██╔════╝██╔════╝
# █████╗  ██║██║     █████╗  ███████╗
# ██╔══╝  ██║██║     ██╔══╝  ╚════██║
# ██║     ██║███████╗███████╗███████║
# ╚═╝     ╚═╝╚══════╝╚══════╝╚══════╝


async def send_images_batch(target: discord.Interaction | discord.Message, urls: list[str]):
    """
    Downloads a list of image URLs and sends them to Discord in batches of up to 10 files.

    Args:
        target (discord.Message | discord.Interaction): The message or interaction to respond to.
        urls (list[str]): List of image URLs to download and send.
    """
    batch = []

    for i, url in enumerate(urls, start=1):
        data = await aiohttp_client.download_bytes(url)

        filename = get_string_segment(string=url, split_char="/", i=1)

        batch.append(discord.File(io.BytesIO(data), filename=filename))

        if len(batch) == 10 or i == len(urls):
            await send_response_to_discord(target=target, files=batch)
            batch = []

    logging.info(f"-- {len(urls)} images has been uploaded in reply")


async def send_video(target: discord.Interaction | discord.Message, url, filesize_limit):
    """
    Send video as a Discord response (to either a message or an interaction).

    Args:
        target (discord.Interaction | discord.Message):
            The target to respond to (Discord interaction or message).
        url (str):
            The video URL to download.
        filesize_limit (int):
            Maximum allowed file size in bytes (e.g., Discord's 8 MB limit).
    """
    filename = get_string_segment(string=url, split_char="/", i=2)

    file = await get_video(
        url=url,
        filename=filename,
        file_size_limit=filesize_limit
    )

    await send_response_to_discord(target=target, files=[file])
    logging.info("-- Reddit video has been uploaded in reply")


async def send_medias_response(target: discord.Interaction | discord.Message ,medias: list[str]):
    """Dispatches and sends a list of media URLs (Reddit videos, YouTube links, or images) to Discord."""
    pattern = REGEX['youtube']['pattern']
    is_video = medias[0].split('?')[0].endswith(".mp4")

    # --- Reddit video ---
    if is_video :

        if target.guild is None:
            filesize_limit = 10 * 1024 * 1024
        else:
            filesize_limit = target.guild.filesize_limit

        await send_video(
            target=target,
            url=medias[0],
            filesize_limit=filesize_limit
        )

    # --- Youtube video ---
    elif matches_pattern(pattern, medias[0]):
        await send_response_to_discord(target=target, content=medias[0])

    # --- One or multiples images ---
    else:
        await send_images_batch(target=target, urls=medias)


async def reply_with_medias(target: discord.Interaction | discord.Message, url: str):
    """Fetches and replies to a Reddit post by sending its associated media to Discord."""
    responses_strings = STRINGS['reddit']

    medias = await fetch_reddit_medias(url=url)
    if not medias:
        return

    await send_response_to_discord(
        target=target,
        content=responses_strings['reply_message_with_medias_count'].format(medias_count=len(medias))
    )

    # --- Send all medias ---
    await send_medias_response(target=target, medias=medias)
