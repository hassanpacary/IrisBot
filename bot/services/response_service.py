"""
bot/services/response_service.py
© by hassanpacary

Utility functions for send response to discord user
"""

# --- Imports ---
import io
import logging

# --- Third party imports ---
import discord

# --- Bot modules ---
from bot.core.config_loader import STRINGS, REGEX
from bot.services.reddit_service import fetch_reddit_data
from bot.services.video_service import get_video
from bot.utils.aiohttp_client import aiohttp_client
from bot.utils.discord_utils import send_response_to_discord, create_discord_embed
from bot.utils.strings_utils import matches_pattern, get_string_segment


# ███████╗██╗██╗     ███████╗███████╗
# ██╔════╝██║██║     ██╔════╝██╔════╝
# █████╗  ██║██║     █████╗  ███████╗
# ██╔══╝  ██║██║     ██╔══╝  ╚════██║
# ██║     ██║███████╗███████╗███████║
# ╚═╝     ╚═╝╚══════╝╚══════╝╚══════╝


async def send_images_batch(
        target: discord.Interaction | discord.Message,
        urls: list[str],
        message_content: str,
        message_embed: discord.Embed,
):
    """
    Downloads a list of image URLs and sends them to Discord in batches of up to 10 files

    Parameters:
        target (discord.Message | discord.Interaction): The message or interaction to respond to
        urls (list[str]): List of image URLs to download and send
        message_content (str): Content to send
        message_embed (discord.Embed): Discord embed to send
    """
    batch = []

    await send_response_to_discord(target=target, content=message_content, embed=message_embed)

    for i, url in enumerate(urls, start=1):
        data = await aiohttp_client.download_bytes(url)

        filename = get_string_segment(string=url, split_char="/", i=1)

        batch.append(discord.File(io.BytesIO(data), filename=filename))

        if len(batch) == 10 or i == len(urls):
            await send_response_to_discord(target=target, files=batch, detach=True)
            batch = []

    logging.info(f"-- {len(urls)} images has been uploaded in reply")


async def send_video(
        target: discord.Interaction | discord.Message,
        url: str,
        filesize_limit: int,
        message_content: str,
        message_embed: discord.Embed,
):
    """
    Send video as a Discord response

    Parameters:
        target (discord.Interaction | discord.Message): The target to respond to (Discord interaction or message)
        url (str): The video URL to download
        filesize_limit (int): Maximum allowed file size in bytes (e.g., Discord's 10 MB limit)
        message_content (str): message content
        message_embed (discord.Embed): message embed
    """
    filename = get_string_segment(string=url, split_char="/", i=2)

    file = await get_video(url=url, filename=filename, file_size_limit=filesize_limit)

    await send_response_to_discord(target=target, content=message_content, embed=message_embed)
    await send_response_to_discord(target=target, files=[file], detach=True)
    logging.info("-- Reddit video has been uploaded in reply")


async def send_medias_response(
        target: discord.Interaction | discord.Message ,
        medias: list[str],
        message_content: str,
        message_embed: discord.Embed,
):
    """
    Dispatches and sends a list of media URLs (Reddit videos, YouTube links, or images) to Discord

    Parameters:
        target (discord.Interaction | discord.Message): The target to respond to (Discord interaction or message)
        medias (list[str]): List of media URLs to send
        message_content (str): message content
        message_embed (discord.Embed): message embed
    """
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
            filesize_limit=filesize_limit,
            message_content=message_content,
            message_embed=message_embed,
        )

    # --- Youtube video ---
    elif matches_pattern(pattern, medias[0]):
        await send_response_to_discord(
            target=target,
            content=message_content + "\n" + medias[0],
            embed=message_embed
        )

    # --- One or multiples images ---
    else:
        await send_images_batch(
            target=target,
            urls=medias,
            message_content=message_content,
            message_embed=message_embed,
        )


async def reply_with_medias(target: discord.Interaction | discord.Message, url: str):
    """
    Fetches and replies to a Reddit post by sending its associated media to Discord

    Parameters:
        target (discord.Interaction | discord.Message): The target to respond to (Discord interaction or message)
        url (str): The url of reddit submission for retrieve their data
    """
    defer_msg = None
    strings = STRINGS['reddit']

    # Send defer message
    if isinstance(target, discord.Interaction):
        await target.response.defer() # type: ignore
    elif isinstance(target, discord.Message):
        defer_msg = await target.channel.send(STRINGS['system']['progress'])

    submission_data = await fetch_reddit_data(url=url)
    medias = submission_data['medias']
    if not medias:
        return

    # Prepare message content
    message_content = strings['reply_message_with_medias_count'].format(medias_count=len(medias))
    message_embed = await create_discord_embed(
        color=discord.Color(0xFF4500),
        title=submission_data['post_title'],
        title_url=submission_data['post_url'],
        description=submission_data['post_content'],
        date=submission_data['creation_date'],
        author="r/" + submission_data['subreddit_name'],
        icon=submission_data['subreddit_icon'],
        fields=[
            (strings['embed_fields']['author'], submission_data['author_name']),
            (strings['embed_fields']['upvote'], submission_data['upvote_number']),
            (strings['embed_fields']['responses'], submission_data['responses_number']),
        ],
        thumbnail_url=submission_data['subreddit_icon'],
        footer_text="Reddit"
    )

    # --- Send responses with medias ---
    await send_medias_response(
        target=target,
        medias=medias,
        message_content=message_content,
        message_embed=message_embed,
    )

    if defer_msg:
        await defer_msg.delete()
