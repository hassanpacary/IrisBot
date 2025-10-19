"""
bot/services/reddit/medias_dispatcher.py
© by hassanpacary

Utility functions for send reddit submission data to user
"""

# --- Imports ---
import logging

# --- Third party imports ---
import discord

# --- Bot modules ---
from bot.core.config_loader import REGEX
from bot.services.reddit.video_compressor import get_video
from bot.utils.aiohttp_client import aiohttp_client
from bot.utils.discord_utils import send_response_to_discord, create_discord_file
from bot.utils.strings_utils import get_string_segment, matches_pattern


# ██████╗ ██╗███████╗██████╗  █████╗ ████████╗ ██████╗██╗  ██╗███████╗██████╗
# ██╔══██╗██║██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██║  ██║██╔════╝██╔══██╗
# ██║  ██║██║███████╗██████╔╝███████║   ██║   ██║     ███████║█████╗  ██████╔╝
# ██║  ██║██║╚════██║██╔═══╝ ██╔══██║   ██║   ██║     ██╔══██║██╔══╝  ██╔══██╗
# ██████╔╝██║███████║██║     ██║  ██║   ██║   ╚██████╗██║  ██║███████╗██║  ██║
# ╚═════╝ ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝


async def _send_images_batch(
        ctx: discord.Interaction | discord.Message,
        urls: list[str],
        message_content: str,
        message_embed: discord.Embed,
):
    """
    Downloads a list of image URLs and sends them to Discord in batches of up to 10 files

    Parameters:
        ctx (discord.Message | discord.Interaction): The message or interaction to respond to
        urls (list[str]): List of image URLs to download and send
        message_content (str): Content to send
        message_embed (discord.Embed): Discord embed to send
    """
    batch = []

    await send_response_to_discord(ctx=ctx, content=message_content, embed=message_embed)

    for i, url in enumerate(urls, start=1):
        data = await aiohttp_client.download_bytes(url)

        filename = get_string_segment(string=url, split_char="/", i=1)

        file = await create_discord_file(filename=filename, data=data)
        batch.append(file)

        if len(batch) == 10 or i == len(urls):
            await send_response_to_discord(ctx=ctx, files=batch, detach=True)
            batch = []

    logging.info(
        "-- %s images has been uploaded in reply",
        len(urls)
    )


async def _send_video(
        ctx: discord.Interaction | discord.Message,
        url: str,
        filesize_limit: int,
        message_content: str,
        message_embed: discord.Embed,
):
    """
    Send video as a Discord response

    Parameters:
        ctx (discord.Interaction | discord.Message):
            The target to respond to (Discord interaction or message)
        url (str): The video URL to download
        filesize_limit (int): Maximum allowed file size in bytes (e.g., Discord's 10 MB limit)
        message_content (str): message content
        message_embed (discord.Embed): message embed
    """
    filename = get_string_segment(string=url, split_char="/", i=2)

    file = await get_video(url=url, filename=filename, file_size_limit=filesize_limit)

    await send_response_to_discord(ctx=ctx, content=message_content, embed=message_embed)
    await send_response_to_discord(ctx=ctx, files=[file], detach=True)
    logging.info("-- Reddit video has been uploaded in reply")


async def dispatch_medias_response(
        ctx: discord.Interaction | discord.Message ,
        medias: list[str],
        message_content: str,
        message_embed: discord.Embed,
):
    """
    Dispatches and sends a list of media URLs
    (Reddit videos, YouTube links, or images) to Discord

    Parameters:
        ctx (discord.Interaction | discord.Message):
                The target to respond to (Discord interaction or message)
        medias (list[str]): List of media URLs to send
        message_content (str): message content
        message_embed (discord.Embed): message embed
    """
    pattern = REGEX['youtube']['pattern']
    is_video = medias[0].split('?')[0].endswith(".mp4")

    # --- Reddit video ---
    if is_video :

        if ctx.guild is None:
            filesize_limit = 10 * 1024 * 1024
        else:
            filesize_limit = ctx.guild.filesize_limit

        await _send_video(
            ctx=ctx,
            url=medias[0],
            filesize_limit=filesize_limit,
            message_content=message_content,
            message_embed=message_embed,
        )

    # --- Youtube video ---
    elif matches_pattern(pattern, medias[0]):
        await send_response_to_discord(
            ctx=ctx,
            content=message_content + "\n" + medias[0],
            embed=message_embed
        )

    # --- One or multiples images ---
    else:
        await _send_images_batch(
            ctx=ctx,
            urls=medias,
            message_content=message_content,
            message_embed=message_embed,
        )
