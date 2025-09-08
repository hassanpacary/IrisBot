"""
bot/services/reddit_service.py
© by hassanpacary

Useful services for fetching images from Reddit posts and sending them to Discord.
"""

# --- Imports ---
import os

# --- Third party imports ---
import asyncpraw

# --- bot modules ---
from bot.utils.aiohttp_client import aiohttp_client
from bot.utils.files_utils import load_json
from bot.utils.strings_utils import matches_pattern

# --- Load json config files ---
BOT = load_json(os.path.join("bot", "config", "bot.json"))
STRINGS = load_json(os.path.join("bot", "config", f"strings.{BOT['langage']}.json"))
REGEX = load_json(os.path.join("bot", "config", "regex.json"))


# ██████╗ ███████╗██████╗ ██████╗ ██╗████████╗    ███████╗███████╗██████╗ ██╗   ██╗██╗ ██████╗███████╗
# ██╔══██╗██╔════╝██╔══██╗██╔══██╗██║╚══██╔══╝    ██╔════╝██╔════╝██╔══██╗██║   ██║██║██╔════╝██╔════╝
# ██████╔╝█████╗  ██║  ██║██║  ██║██║   ██║       ███████╗█████╗  ██████╔╝██║   ██║██║██║     █████╗
# ██╔══██╗██╔══╝  ██║  ██║██║  ██║██║   ██║       ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██║██║     ██╔══╝
# ██║  ██║███████╗██████╔╝██████╔╝██║   ██║       ███████║███████╗██║  ██║ ╚████╔╝ ██║╚██████╗███████╗
# ╚═╝  ╚═╝╚══════╝╚═════╝ ╚═════╝ ╚═╝   ╚═╝       ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚═╝ ╚═════╝╚══════╝


def create_reddit_client() -> asyncpraw.Reddit:
    """Creates and returns an asyncpraw Reddit client using environment variables."""
    return asyncpraw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ["REDDIT_USER_AGENT"]
    )


async def extract_submission_medias(submission) -> list[str]:
    """
    Extracts all media URLs from a Reddit submission, including videos, galleries, and images.

    Args:
        submission (asyncpraw.models.Submission): The Reddit submission object.

    Returns:
        list[str]: List of media URLs.
    """
    pattern = REGEX['youtube']['pattern']
    medias = []

    # --- Reddit video ---
    if getattr(submission, "is_video", False):
        medias.append(submission.media["reddit_video"]["fallback_url"])

    # --- Reddit gallery ---
    elif hasattr(submission, "gallery_data"):
        for item in submission.gallery_data["items"]:
            media_id = item["media_id"]
            meta = submission.media_metadata[media_id]
            medias.append(meta["s"]["u"])

    # --- single image or YouTube link ---
    else:
        url = submission.url

        async with aiohttp_client.session.head(url, timeout=5) as resp:
            content_type = resp.headers.get("Content-Type", "")

            if content_type.startswith("image/") or matches_pattern(pattern, url):
                medias.append(url)

    return medias


async def fetch_reddit_medias(url: str) -> list[str]:
    """
    Fetches media URLs from a given Reddit post.

    Returns:
        list[str]: A list of media URLs extracted from the submission.
    """

    # --- Create Reddit client ---
    reddit_client = create_reddit_client()

    submission = await reddit_client.submission(url=url)
    medias = await extract_submission_medias(submission=submission)

    return medias
