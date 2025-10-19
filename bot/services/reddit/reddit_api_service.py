"""
bot/services/reddit/reddit_service.py
© by hassanpacary

Utility functions for fetching images from Reddit posts and sending them to Discord
"""

# --- Imports ---
import os
from datetime import datetime

# --- Third party imports ---
import asyncpraw

# --- bot modules ---
from bot.core.config_loader import REGEX
from bot.utils.aiohttp_client import aiohttp_client
from bot.utils.strings_utils import matches_pattern


# pylint: disable=line-too-long
# ██████╗ ███████╗██████╗ ██████╗ ██╗████████╗    ███████╗███████╗██████╗ ██╗   ██╗██╗ ██████╗███████╗
# ██╔══██╗██╔════╝██╔══██╗██╔══██╗██║╚══██╔══╝    ██╔════╝██╔════╝██╔══██╗██║   ██║██║██╔════╝██╔════╝
# ██████╔╝█████╗  ██║  ██║██║  ██║██║   ██║       ███████╗█████╗  ██████╔╝██║   ██║██║██║     █████╗
# ██╔══██╗██╔══╝  ██║  ██║██║  ██║██║   ██║       ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██║██║     ██╔══╝
# ██║  ██║███████╗██████╔╝██████╔╝██║   ██║       ███████║███████╗██║  ██║ ╚████╔╝ ██║╚██████╗███████╗
# ╚═╝  ╚═╝╚══════╝╚═════╝ ╚═════╝ ╚═╝   ╚═╝       ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚═╝ ╚═════╝╚══════╝
# pylint: enable=line-too-long


def _create_reddit_client() -> asyncpraw.Reddit:
    """
    Creates and returns an asyncpraw Reddit client using environment variables

    Returns:
        asyncpraw.reddit.Reddit client
    """
    return asyncpraw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ["REDDIT_USER_AGENT"]
    )


async def _extract_submission_data(submission) -> dict:
    """
    Extracts data from submission data with media URLs from a Reddit submission

    Parameters:
        submission (asyncpraw.models.Submission): The Reddit submission object.

    Returns:
        list[str]: List of all submission data
    """
    pattern = REGEX['youtube']['pattern']

    post_created_date = datetime.fromtimestamp(submission.created_utc)

    # Load the subreddit object
    subreddit = submission.subreddit
    await subreddit.load()

    # All submissions data retrieve
    submission_data = {
        "post_title": submission.title,
        "post_url": submission.url,
        "post_content": submission.selftext,
        "creation_date": post_created_date,
        "subreddit_name": subreddit.display_name,
        "author_name": getattr(submission.author, "name", "") or "",
        "subreddit_icon": subreddit.icon_img,
        "upvote_number": submission.score,
        "responses_number": submission.num_comments,
        "medias": []
    }

    # --- Reddit video ---
    if getattr(submission, "is_video", False):
        submission_data['medias'].append(submission.media["reddit_video"]["fallback_url"])

    # --- Reddit gallery ---
    elif hasattr(submission, "gallery_data"):
        for item in submission.gallery_data["items"]:
            media_id = item["media_id"]
            meta = submission.media_metadata[media_id]
            submission_data['medias'].append(meta["s"]["u"])

    # --- single image or YouTube link ---
    else:
        url = submission.url

        async with aiohttp_client.session.head(url, timeout=5) as resp:
            content_type = resp.headers.get("Content-Type", "")

            if content_type.startswith("image/") or matches_pattern(pattern, url):
                submission_data['medias'].append(url)

    return submission_data


async def fetch_reddit_data(url: str) -> dict:
    """
    Fetches reddit submission data from a given Reddit post

    Parameters:
        url (str): Reddit post url

    Returns:
        list[str]: A list of data extracted from the submission.
    """

    # --- Create Reddit client ---
    reddit_client = _create_reddit_client()

    submission = await reddit_client.submission(url=url)
    submission_data = await _extract_submission_data(submission=submission)

    return submission_data
