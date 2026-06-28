"""Reddit API requests using asyncpraw.

Fetches Reddit submission data including post metadata and media URLs,
from Reddit API using asyncpraw.

The Reddit client is opened as an async context manager per request.

If Asyncpraw request return wrong data or attributes don't match, so the Reddit
API attributes as changed. For test this use 'pprint.pprint(vars(submission))' for
view all attributes of the API.

© by hassanpacary
"""

# --- Standard library ---
from datetime import datetime

# --- Third-party ---
import asyncpraw

# --- Internal ---
from bot.core import environment


def _create_reddit_client() -> asyncpraw.Reddit:
    """Creates an asyncpraw Reddit client from environment variables.

    Returns:
        A configured asyncpraw.Reddit instance.
    """
    return asyncpraw.Reddit(
        client_id=environment.get_env_var("REDDIT_CLIENT_ID"),
        client_secret=environment.get_env_var("REDDIT_CLIENT_SECRET"),
        user_agent=environment.get_env_var("REDDIT_USER_AGENT"),
    )


async def _extract_medias_urls(submission) -> list[str]:
    """Extracts all media URLs from a Reddit submission.

    Handles three media types:
      - Reddit-hosted video: extracts the video fallback URL.
      - Gallery posts: extracts the full-size image URL for each gallery item (image).
      - Single URL: Image, GIF or also YouTube links.

    Args:
        submission: An asyncpraw Submission instance.

    Returns:
        A list of media URL strings. Empty if no recognizable media is found.
    """
    medias: list[str] = []

    # Is video if submission as attribute 'is_video' set to True
    if getattr(submission, "is_video", False):
        medias.append(submission.media["reddit_video"]["fallback_url"])

    # Is Gallery if submission as attribute 'is_gallery' set to True
    elif getattr(submission, "is_gallery", False):
        for item in submission.gallery_data["items"]:
            media_id = item["media_id"]
            meta = submission.media_metadata[media_id]
            medias.append(meta["s"]["u"])

    # Is another post_hint like: "image", "rich:video" or also link.
    # Attribute post_hint refer to the media type.
    else:
        medias.append(submission.url_overridden_by_dest or submission.url)

    return medias


async def _extract_submission_data(submission) -> dict:
    """Extracts and structures metadata and media URLs from a Reddit submission.

    Loads the subreddit lazily to access display_name and icon_img,
    then delegates media extraction to _extract_medias_urls().

    Args:
        submission: An asyncpraw Submission instance.

    Returns:
        A dict containing post and subreddit metadata and media URLs.
    """
    subreddit = submission.subreddit
    await subreddit.load()

    medias = await _extract_medias_urls(submission)

    return {
        "post_title": submission.title,
        "post_url": submission.shortlink,
        "post_content": submission.selftext,
        "creation_date": datetime.fromtimestamp(submission.created_utc),
        "subreddit_name": subreddit.display_name,
        "author_name": getattr(submission.author, "name", "") or "",
        "subreddit_icon": subreddit.icon_img,
        "upvote_number": submission.score,
        "responses_number": submission.num_comments,
        "medias": medias,
    }


# --- Exposed functions ---


async def fetch_post(url: str) -> dict:
    """Fetches submission data from a Reddit post URL.

    Args:
        url: The Reddit post URL to fetch.

    Returns:
        A dict containing post metadata and media URLs.
    """
    async with _create_reddit_client() as session:
        submission = await session.submission(url=url)
    return await _extract_submission_data(submission=submission)
