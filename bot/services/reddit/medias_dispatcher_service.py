"""Medias dispatcher service for reddit cog.

Manage logics functions for dispatch Reddit post media (videos, YouTube links, images)
to the appropriate Discord upload strategy.

© by hassanpacary
"""

# --- Standard library ---
import io
import logging
import re

# --- Third-party ---
import aiohttp
import discord

# --- Internal ---
from bot.config import regex_config
from bot.services.reddit import video_compressor
from bot.utils.strings_utils import get_string_segment

# --- Constants ---
_DEFAULT_FILESIZE_LIMIT: int = 10 * 1024 * 1024
_MAX_FILES_PER_MESSAGE: int = 10


async def _send_images(
        channel: discord.TextChannel,
        urls: list[str],
) -> None:
    """Downloads and sends images in batches of up to 10 per message.

    If a single image fails to download, logs a warning and continues.

    Args:
        channel: The discord channel to send the media to.
        urls: A list of image URLs to download and send.
    """
    batch: list[discord.File] = []

    for i, url in enumerate(urls, start=1):
        try:
            async with aiohttp.ClientSession() as session:
                resp = await session.get(url=url)
                image_bytes = await resp.read()

            filename = get_string_segment(string=url, split_char="/", i=1)
            file = discord.File(
                fp=io.BytesIO(image_bytes),
                filename=filename,
            )

            batch.append(file)
        except aiohttp.ClientError as e:
            logging.warning("Failed to download image %s: %s",url, e)
            continue

        if len(batch) == _MAX_FILES_PER_MESSAGE or i == len(urls):
            await channel.send(files=batch)
            batch = []

    logging.info("%s image(s) uploaded", len(urls))


async def _send_video(
        ctx: discord.Interaction | discord.Message,
        channel: discord.TextChannel,
        url: str,
) -> None:
    """Sends the video of the Reddit post.

    The process for getting the video pass by video_compressor utilities functions.
    Download and processes (compress the video if too large for discord).

    Args:
        ctx: The Discord interaction or message context.
        channel: The discord channel to send the media to.
        url: The Reddit video stream URL.

    Raises:
        ValueError: If the video precessing failed.
    """
    filesize_limit = getattr(
        ctx.guild,
        "filesize_limit",
        _DEFAULT_FILESIZE_LIMIT,
    )

    file = await video_compressor.get_video(url=url, file_size_limit=filesize_limit)
    if file is not None:
        await channel.send(file=file)
        logging.info("Video of the Reddit post uploaded.")
    else:
        raise ValueError("Reddit video processing failed, skipping upload.")


async def dispatch_medias_upload_strategy(
        ctx: discord.Interaction | discord.Message,
        medias: list[str],
        channel: discord.TextChannel
) -> None:
    """Routes the list of medias to the appropriate Discord upload strategy.

    Handles three cases: Reddit video (.mp4), YouTube link, or images.

    Args:
        ctx: The Discord interaction or message context.
        medias: A non-empty list of media URLs from the Reddit post.
        channel: The discord channel to send the media to.
    """
    first_media = medias[0]
    is_video = first_media.split("?")[0].endswith(".mp4")

    if re.match(pattern=regex_config.YOUTUBE_URL, string=first_media):
        await channel.send(content=first_media)
    elif is_video:
        await _send_video(ctx=ctx, url=first_media, channel=channel)
    else:
        await _send_images(channel=channel, urls=medias)
