"""
reddit_utils.py

This module allows fetching images from Reddit posts and sending them to Discord.

Functions:
- fetch_reddit_images(url: str) -> list[str]:
    Fetches all image URLs from a Reddit post.
- reply_reddit(self, message: discord.Message, url: str):
    Fetches images from a Reddit post and replies in Discord.
- send_reddit_images(images: list[str], message: discord.Message = None, interaction: discord.Interaction = None):
    Sends Reddit images in Discord in batches, either via a message or an interaction.
"""
from typing import Any, Coroutine

import aiohttp
import asyncpraw
import discord
import io
import os
from config.constants import IMAGE_EXTENSIONS
from config.string_fr import REDDIT_RESPONSE_MESSAGE
from config.regex import YOUTUBE_URL_REGEX


# Client Reddit
reddit_client = asyncpraw.Reddit(
    client_id=os.environ["REDDIT_CLIENT_ID"],
    client_secret=os.environ["REDDIT_CLIENT_SECRET"],
    user_agent=os.environ["REDDIT_USER_AGENT"]
)


async def fetch_reddit_medias(url: str) -> list[Any]:
    """
    Fetch all image URLs from a Reddit post.

    Args:
        url (str): The Reddit post URL.

    Returns:
        list[str]: A list of image URLs (can be empty if no images found).
    """
    submission = await reddit_client.submission(url=url)
    medias = []

    print(submission.url)
    # Single image
    if submission.url.endswith(IMAGE_EXTENSIONS):
        medias.append(submission.url)

    # Gallery
    if hasattr(submission, "gallery_data"):
        for item in submission.gallery_data["items"]:
            media_id = item["media_id"]
            meta = submission.media_metadata[media_id]
            image_url = meta["s"]["u"]
            medias.append(image_url)

    # Youtube video
    if YOUTUBE_URL_REGEX.match(submission.url):
        medias.append(submission.url)

    print(medias)
    return medias


async def send_reddit_medias(medias: list[str], message: discord.Message = None, interaction: discord.Interaction = None):
    """
    Send Reddit images in batches of 10 to a Discord channel.

    Args:
        medias (list[str]): A list of image URLs.
        message(discord.Message): The Discord message object.
        interaction (discord.Interaction): The interaction to send the images to.
    """

    # Open aiohttp session for execute multiple http requests
    async with aiohttp.ClientSession() as session:
        if YOUTUBE_URL_REGEX.match(medias[0]):
            youtube_url = medias[0]
            if interaction:
                await interaction.followup.send(youtube_url)
                return
            elif message:
                await message.reply(youtube_url)
                return

        batch = []
        for i, url in enumerate(medias, start=1):
            filename = f"media_{i}"

            # retrieves all images from their URL and saves them in a batch
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.read()
                    file = discord.File(io.BytesIO(data), filename=filename + '.jpg')
                    batch.append(file)

                    # Send message with images in discord.TextCannel ou discord.DMChannel when batch size is up to 10
                    if len(batch) == 10 or i == len(medias):
                        if interaction:
                            await interaction.followup.send(files=batch)
                        elif message:
                            await message.reply(files=batch)
                        batch = []


async def reply_reddit(self, message: discord.Message, url: str):
    """
    Fetch images from a Reddit post and reply to a Discord message with them.

    Workflow:
        1. Fetches all images from the Reddit URL.
        2. Sends a confirmation message as a reply to the original message, including the number of images.
        3. If images are found, sends them in batches as replies to the bot's confirmation message.
        4. Ensures that other bot commands are still processed after handling.

    Args:
        self: Self
        message (discord.Message): The message sent by a user containing the Reddit URL.
        url (str): The Reddit post URL to fetch images from.
    """
    medias = await fetch_reddit_medias(url=url)

    bot_msg = await message.reply(REDDIT_RESPONSE_MESSAGE.format(medias_count=len(medias)))

    if medias:
        await send_reddit_medias(message=bot_msg, medias=medias)

    await self.bot.process_commands(message)