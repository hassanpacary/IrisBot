"""Reddit service for reddit cog.

Manage logics functions for reddit url pattern command and listener.
Sends improved Reddit post embed followed by the post medias

© by hassanpacary
"""

# --- Standard library ---
import logging
import re

# --- Third-party ---
import discord

# --- Internal ---
from bot.api.reddit import reddit_api_requests
from bot.cogs.reddit import reddit_strings
from bot.config import colors_config, regex_config
from bot.services.reddit import medias_dispatcher_service
from bot.utils import discord_utils


async def _build_reddit_embed(submission_data: dict) -> discord.Embed:
    """Builds a Discord embed from Reddit submission metadata.

    Args:
        submission_data: A dict of post metadata as returned by fetch_reddit_data.

    Returns:
        A fully constructed discord.Embed instance.
    """
    return await discord_utils.create_discord_embed(
        color=discord.Color(int(colors_config.Utils.REDDIT, 16)),
        title=submission_data['post_title'],
        title_url=submission_data['post_url'],
        description=submission_data['post_content'],
        date=submission_data['creation_date'],
        author=f"r/{submission_data['subreddit_name']}",
        icon=submission_data['subreddit_icon'],
        fields=[
            (reddit_strings.RedditEmbedFields.AUTHOR, submission_data['author_name']),
            (reddit_strings.RedditEmbedFields.UPVOTE, submission_data['upvote_number']),
            (
                reddit_strings.RedditEmbedFields.RESPONSES,
                submission_data['responses_number'],
            ),
        ],
        thumbnail_url=submission_data['subreddit_icon'],
        footer_text=reddit_strings.RedditEmbedFields.FOOTER,
    )


async def _send_improved_embed(
        ctx: discord.Interaction | discord.Message,
        url: str,
) -> None:
    """Sends the embed and dispatches any media
    (video, images, YouTube) as follow-ups.

    Args:
        ctx: The Discord interaction or message context.
        url: The Reddit post URL to embed.
    """
    if not isinstance(ctx.channel, discord.TextChannel):
        return

    channel = await discord_utils.get_channel_by_ctx(ctx=ctx, channel_id=ctx.channel.id)

    async with channel.typing():
        if isinstance(ctx, discord.Interaction):
            await ctx.response.defer()

        submission_data = await reddit_api_requests.fetch_post(url=url)
        medias = submission_data['medias']
        embed = await _build_reddit_embed(submission_data=submission_data)

        if isinstance(ctx, discord.Interaction):
            await ctx.followup.send(
                content=reddit_strings.RESPONSE,
                embed=embed,
            )
        else:
            await ctx.edit(suppress=True)
            await channel.send(content=reddit_strings.RESPONSE, embed=embed)

        if medias:
            await medias_dispatcher_service.dispatch_medias_upload_strategy(
                ctx=ctx,
                medias=medias,
                channel=channel,
            )


async def handle_reddit_url_message(message: discord.Message, url: str) -> None:
    """Replies with improved Reddit post embed and the medias of the post.

    Args:
        message: The incoming Discord message to evaluate.
        url: The Reddit post URL to embed.
    """
    await _send_improved_embed(ctx=message, url=url)
    logging.info(
        "%s said: '%s' and matched with reddit post url pattern.",
        message.author,
        message.content,
    )


async def handle_reddit_url(interaction: discord.Interaction, url: str) -> None:
    """Replies with improved Reddit post embed and the medias of the Reddit post.

    in the case URL don't match, responds to the user with ephemeral message.

    Args:
        interaction: The Discord interaction context.
        url: The Reddit post URL to embed.
    """
    matched_object = re.search(
        pattern=regex_config.REDDIT_URL,
        string=url
    )

    if matched_object:
        await _send_improved_embed(ctx=interaction, url=url)
    else:
        await interaction.response.send_message(content=reddit_strings.WRONG_URL)
