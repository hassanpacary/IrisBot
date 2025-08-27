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


import aiohttp
import asyncpraw
import discord
import io
import os
from config.constants import IMAGE_EXTENSIONS
from config.string_fr import REDDIT_RESPONSE_MESSAGE


# Client Reddit
reddit_client = asyncpraw.Reddit(
    client_id=os.environ["REDDIT_CLIENT_ID"],
    client_secret=os.environ["REDDIT_CLIENT_SECRET"],
    user_agent=os.environ["REDDIT_USER_AGENT"]
)

async def fetch_reddit_images(url: str) -> list[str]:
    """
    Fetch all image URLs from a Reddit post.

    Args:
        url (str): The Reddit post URL.

    Returns:
        list[str]: A list of image URLs (can be empty if no images found).
    """
    submission = await reddit_client.submission(url=url)
    images = []

    # Single image
    if submission.url.endswith(IMAGE_EXTENSIONS):
        images.append(submission.url)

    # Gallery
    if hasattr(submission, "gallery_data"):
        for item in submission.gallery_data["items"]:
            media_id = item["media_id"]
            meta = submission.media_metadata[media_id]
            image_url = meta["s"]["u"]
            images.append(image_url)

    return images


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
    images = await fetch_reddit_images(url=url)

    bot_msg = await message.reply(REDDIT_RESPONSE_MESSAGE.format(image_count=len(images)))

    if images:
        await send_reddit_images(message=bot_msg, images=images)

    await self.bot.process_commands(message)



async def send_reddit_images(images: list[str], message: discord.Message = None, interaction: discord.Interaction = None):
    """
    Send Reddit images in batches of 10 to a Discord channel.

    Args:
        images (list[str]): A list of image URLs.
        message(discord.Message): The Discord message object.
        interaction (discord.Interaction): The interaction to send the images to.
    """

    # Open aiohttp session for execute multiple http requests
    async with aiohttp.ClientSession() as session:
        batch = []
        for idx, url in enumerate(images, start=1):

            # retrieves all images from their URL and saves them in a batch
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.read()
                    file = discord.File(io.BytesIO(data), filename=f"image_{idx}.jpg")
                    batch.append(file)

            # Send message with images in discord.TextCannem ou discord.DMChannel when batch size is up to 10
            if len(batch) == 10 or idx == len(images):
                if interaction:
                    await interaction.followup.send(files=batch)
                elif message:
                    await message.reply(files=batch)
                batch = []