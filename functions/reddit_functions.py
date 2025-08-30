"""
reddit_functions.py
© by hassanpacary

This module allows fetching images from Reddit posts and sending them to Discord.
"""

# --- Imports ---
import aiohttp
import asyncpraw
import discord
import io
import os
import re
import requests

# --- bot modules ---
from functions.functions import load_json

# Load config data from json files
config = load_json("config.json")
string = load_json(f"string_config_{config['config']['langage']}.json")
regex = load_json("regex_config.json")


async def fetch_reddit_medias(url: str) -> list[str]:
    """
    Fetches media URLs from a given Reddit post.

    Event:
        Triggered when a Reddit URL is provided to retrieve its media content.

    Action:
        - Retrieves the Reddit submission asynchronously using the provided URL.
        - Checks if the submission is a single image and adds it to the media list.
        - If the submission is a gallery, iterates over all items and adds their image URLs.
        - Checks if the submission is a YouTube video and adds the URL.
        - Prints the submission URL and the list of collected media for debugging.

    Returns:
        list[str]: A list of media URLs (images, gallery items, or videos) extracted from the submission.
    """

    # --- Client Reddit ---
    reddit_client = asyncpraw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ["REDDIT_USER_AGENT"]
    )

    submission = await reddit_client.submission(url=url)
    medias = []
    youtube_pattern = re.compile(regex['url_youtube']['pattern'])

    # --- The post contains a single image OR The post contains a YouTube video ---
    r = requests.head(submission.url)
    if r.headers.get('Content-Type').startswith('image/') or youtube_pattern.match(submission.url):
        medias.append(submission.url)

    # --- The post contains a gallery of images ---
    if hasattr(submission, "gallery_data"):
        for item in submission.gallery_data["items"]:
            media_id = item["media_id"]
            meta = submission.media_metadata[media_id]
            image_url = meta["s"]["u"]
            medias.append(image_url)

    return medias


async def send_reddit_medias(medias: list[str], message: discord.Message = None,
                             interaction: discord.Interaction = None):
    """
    Sends a list of media URLs (images or videos) to a Discord channel or interaction.

    Event:
        Triggered when a list of Reddit media URLs is ready to be sent to Discord.

    Action:
        - Opens an asynchronous HTTP session to fetch media content.
        - If the first media URL is a YouTube link, sends it directly to the interaction
          or message and returns.
        - Iterates through all media URLs, retrieves their data, and prepares them as
          Discord files.
        - Sends media in batches of 10 files at a time to avoid exceeding Discord limits.
        - Supports sending to either a `discord.Message` reply or an `interaction.followup`.
    """

    # Open aiohttp session for execute multiple http requests
    async with aiohttp.ClientSession() as session:
        youtube_pattern = re.compile(regex['url_youtube']['pattern'])

        # --- The media list contains only one YouTube video ---
        if youtube_pattern.match(medias[0]):
            youtube_url = medias[0]
            if interaction:
                await interaction.followup.send(youtube_url)
                return
            elif message:
                await message.reply(youtube_url)
                return

        # --- the media list contains one or more images ---
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
    Fetches media from a Reddit URL and replies to the message with the content.

    Event:
        Triggered when the bot needs to respond to a Reddit URL provided in a message.

    Action:
        - Fetches media URLs from the provided Reddit URL using `fetch_reddit_medias`.
        - Sends a reply message indicating the number of media items found.
        - If media is found, sends the media files to the reply using `send_reddit_medias`.
        - Processes other bot commands in the original message after replying.
    """
    medias = await fetch_reddit_medias(url=url)

    bot_msg = await message.reply(string['reddit']['reply_message_with_medias_count'].format(medias_count=len(medias)))

    if medias:
        await send_reddit_medias(message=bot_msg, medias=medias)

    await self.bot.process_commands(message)
