"""
bot/services/moderation/moderation_service.py
© by hassanpacary

Utility functions for general moderation cog
"""

# --- Third party imports ---
import discord
from discord.ext import commands

# --- Bot modules ---
from bot.core.config_loader import BOT, STRINGS
from bot.utils.discord_utils import (create_discord_embed,
                                     send_message_in_channel,
                                     send_response_to_discord)


# ██╗      ██████╗  ██████╗
# ██║     ██╔═══██╗██╔════╝
# ██║     ██║   ██║██║  ███╗
# ██║     ██║   ██║██║   ██║
# ███████╗╚██████╔╝╚██████╔╝
# ╚══════╝ ╚═════╝  ╚═════╝


async def log_deleted_message(ctx: commands.Bot, message: discord.Message):
    """Logic of on_message_delete event"""
    color = BOT['color']['moderation']
    channel_id = BOT['channels']['log']
    guild = STRINGS['system']['guild']
    responses_dict = STRINGS['moderation']['log_component']

    embed = await create_discord_embed(
        color=discord.Color(int(color, 16)),
        title=message.author.name,
        description=message.content,
        date=message.created_at,
        author=responses_dict['embed_delete_message'],
        icon=ctx.user.avatar.url,
        thumbnail_url=message.author.display_avatar.url,
        footer_text=guild
    )

    await send_message_in_channel(ctx=message, channel_id=channel_id, embed=embed)


async def log_edited_message(
        ctx: commands.Bot,
        message_before: discord.Message,
        message_after: discord.Message
):
    """Logic of on_message_edit event"""
    color = BOT['color']['moderation']
    channel_id = BOT['channels']['log']
    guild = STRINGS['system']['guild']
    responses_dict = STRINGS['moderation']['log_component']

    embed = await create_discord_embed(
        color=discord.Color(int(color, 16)),
        title=message_before.author.name,
        description=message_before.content,
        date=message_before.created_at,
        author=responses_dict['embed_edited_message'],
        icon=ctx.user.avatar.url,
        fields=[
            (responses_dict['embed_new_message_field'], message_after.content)
        ],
        thumbnail_url=message_before.author.display_avatar.url,
        footer_text=guild
    )

    await send_message_in_channel(ctx=message_before, channel_id=channel_id, embed=embed)


# ██████╗ ██╗   ██╗██████╗  ██████╗ ███████╗
# ██╔══██╗██║   ██║██╔══██╗██╔════╝ ██╔════╝
# ██████╔╝██║   ██║██████╔╝██║  ███╗█████╗
# ██╔═══╝ ██║   ██║██╔══██╗██║   ██║██╔══╝
# ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗
# ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝


async def purge_messages(ctx: discord.Interaction, amount: int):
    """Logic of /purge command"""
    amount_max = BOT['moderation']['purge_amount_max']
    responses_dict = STRINGS['moderation']['purge_component']

    # --- Messages amount is too high ---
    if amount > amount_max:
        await send_response_to_discord(
            ctx=ctx,
            content=responses_dict['amount_too_high'].format(max=amount_max),
            ephemeral=True
        )

    # --- Purge chat ---
    else:
        await ctx.response.defer(ephemeral=True)  # type: ignore
        await ctx.channel.purge(limit=amount)
        await send_response_to_discord(
            ctx=ctx,
            content=responses_dict['purge_ok'].format(amount=str(amount)),
            ephemeral=True
        )
