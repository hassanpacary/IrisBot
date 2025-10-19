"""
bot/services/reddit/response_service.py
© by hassanpacary

Utility functions for send reddit submission data to user
"""

# --- Third party imports ---
import discord

# --- Bot modules ---
from bot.core.config_loader import STRINGS, REGEX, BOT
from bot.services.reddit.medias_dispatcher import dispatch_medias_response
from bot.services.reddit.reddit_api_service import fetch_reddit_data
from bot.utils.discord_utils import send_response_to_discord, create_discord_embed
from bot.utils.strings_utils import matches_pattern


# pylint: disable=line-too-long
# ███████╗███████╗███╗   ██╗██████╗     ███████╗██╗   ██╗██████╗ ███╗   ███╗██╗███████╗███████╗██╗ ██████╗ ███╗   ██╗    ██████╗  █████╗ ████████╗ █████╗
# ██╔════╝██╔════╝████╗  ██║██╔══██╗    ██╔════╝██║   ██║██╔══██╗████╗ ████║██║██╔════╝██╔════╝██║██╔═══██╗████╗  ██║    ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗
# ███████╗█████╗  ██╔██╗ ██║██║  ██║    ███████╗██║   ██║██████╔╝██╔████╔██║██║███████╗███████╗██║██║   ██║██╔██╗ ██║    ██║  ██║███████║   ██║   ███████║
# ╚════██║██╔══╝  ██║╚██╗██║██║  ██║    ╚════██║██║   ██║██╔══██╗██║╚██╔╝██║██║╚════██║╚════██║██║██║   ██║██║╚██╗██║    ██║  ██║██╔══██║   ██║   ██╔══██║
# ███████║███████╗██║ ╚████║██████╔╝    ███████║╚██████╔╝██████╔╝██║ ╚═╝ ██║██║███████║███████║██║╚██████╔╝██║ ╚████║    ██████╔╝██║  ██║   ██║   ██║  ██║
# ╚══════╝╚══════╝╚═╝  ╚═══╝╚═════╝     ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝
# pylint: enable=line-too-long


async def send_response_with_post_data(ctx: discord.Interaction | discord.Message, url: str):
    """Logic of /waf command and on_message event when reddit url trigger it"""
    color = BOT['color']['reddit']
    responses_dict = STRINGS['reddit']
    pattern = REGEX['reddit']['pattern']

    if not matches_pattern(pattern, url):
        await send_response_to_discord(ctx=ctx, content=responses_dict['wrong_url'], ephemeral=True)
        return

    defer_msg = None

    # Send defer message
    if isinstance(ctx, discord.Interaction):
        await ctx.response.defer() # type: ignore
    elif isinstance(ctx, discord.Message):
        defer_msg = await ctx.channel.send(STRINGS['system']['progress'])

    submission_data = await fetch_reddit_data(url=url)
    medias = submission_data['medias']

    # Prepare message content
    message_content = (
        responses_dict['reply_message_with_medias_count'].format(
            medias_count=len(medias)
        )
    )
    message_embed = await create_discord_embed(
        color=discord.Color(int(color, 16)),
        title=submission_data['post_title'],
        title_url=submission_data['post_url'],
        description=submission_data['post_content'],
        date=submission_data['creation_date'],
        author="r/" + submission_data['subreddit_name'],
        icon=submission_data['subreddit_icon'],
        fields=[
            (responses_dict['embed_fields']['author'], submission_data['author_name']),
            (responses_dict['embed_fields']['upvote'], submission_data['upvote_number']),
            (responses_dict['embed_fields']['responses'], submission_data['responses_number']),
        ],
        thumbnail_url=submission_data['subreddit_icon'],
        footer_text="Reddit"
    )

    # --- Submission contains medias ---
    if len(medias) > 0:
        # Send responses with medias
        await dispatch_medias_response(
            ctx=ctx,
            medias=medias,
            message_content=message_content,
            message_embed=message_embed,
        )

    # --- Submission contains not medias ---
    else:
        await send_response_to_discord(
            ctx=ctx,
            content=message_content,
            embed=message_embed
        )

    if defer_msg:
        await defer_msg.delete()
