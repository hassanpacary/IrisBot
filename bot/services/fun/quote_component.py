"""
bot/services/fun/quote_service.py
© by hassanpacary

Utility functions for quoting users
"""

# --- Imports ---
from datetime import datetime

from dateutil.relativedelta import relativedelta

# --- Third party imports ---
import discord
from discord.ext import commands

# --- Bot modules ---
from bot.core.config_loader import BOT, STRINGS
from bot.utils.discord_utils import (create_discord_embed,
                                     send_response_to_discord,
                                     create_discord_file)


# pylint: disable=line-too-long
#  ██████╗ ██╗   ██╗ ██████╗ ████████╗███████╗    ███████╗███████╗██████╗ ██╗   ██╗██╗ ██████╗███████╗
# ██╔═══██╗██║   ██║██╔═══██╗╚══██╔══╝██╔════╝    ██╔════╝██╔════╝██╔══██╗██║   ██║██║██╔════╝██╔════╝
# ██║   ██║██║   ██║██║   ██║   ██║   █████╗      ███████╗█████╗  ██████╔╝██║   ██║██║██║     █████╗
# ██║▄▄ ██║██║   ██║██║   ██║   ██║   ██╔══╝      ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██║██║     ██╔══╝
# ╚██████╔╝╚██████╔╝╚██████╔╝   ██║   ███████╗    ███████║███████╗██║  ██║ ╚████╔╝ ██║╚██████╗███████╗
#  ╚══▀▀═╝  ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝    ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚═╝ ╚═════╝╚══════╝
# pylint: enable=line-too-long


async def quote_user_message(ctx: discord.Interaction, message: discord.Message):
    """
    Quote a message in an embed message

    Parameters:
        ctx (discord.Interaction): The interaction with the user who issued the command
        message (discord.Message): The message to quote
    """
    color = BOT['color']['fun']
    responses_dict = STRINGS['fun']['quote_component']
    quotes_channel_id = BOT['channels']['quotes']

    guild = await ctx.client.fetch_guild(BOT['guild_dev'])
    channel = await guild.fetch_channel(quotes_channel_id)

    embed_of_message_quoted = await create_discord_embed(
        color=discord.Color(int(color,16)),
        title=message.author.display_name,
        description=message.content,
        date=message.created_at,
        author=responses_dict['origine'].format(user=ctx.user.display_name),
        icon=ctx.user.avatar.url,
        fields=[
            ("", ctx.user.mention),
            ("", message.author.mention),
        ],
        thumbnail_url=message.author.avatar.url,
        footer_text=responses_dict['embed_footer']
    )

    await channel.send(embed=embed_of_message_quoted)
    await send_response_to_discord(ctx=ctx, content=responses_dict['response'])


async def quote_user_with_screen(ctx: discord.Interaction, screen: discord.Attachment):
    """
    Quote a user with a screen in an embed message

    Parameters:
        ctx (discord.Interaction): The interaction with the user who issued the command
        screen (discord.Attachment): The screen to quote
    """
    color = BOT['color']['fun']
    responses_dict = STRINGS['fun']['quote_component']
    quotes_channel_id = BOT['channels']['quotes']

    guild = await ctx.client.fetch_guild(BOT['guild_dev'])
    channel = await guild.fetch_channel(quotes_channel_id)

    embed_of_message_quoted = await create_discord_embed(
        color=discord.Color(int(color,16)),
        author=responses_dict['origine'].format(user=ctx.user.display_name),
        icon=ctx.user.avatar.url,
        image_url=screen.url,
        footer_text=responses_dict['embed_footer']
    )

    await channel.send(embed=embed_of_message_quoted)
    await send_response_to_discord(ctx=ctx, content=responses_dict['response'])


async def quote_user_with_reaction(ctx: commands.Bot, payload: discord.RawReactionActionEvent):
    """
    Quote a user with a reaction in an embed message

    Parameters:
        ctx (commands.Bot): The bot
        payload (discord.RawReactionActionEvent): The payload to quote
    """
    color = BOT['color']['fun']
    responses_dict = STRINGS['fun']['quote_component']
    quotes_channel_id = BOT['channels']['quotes']

    guild = ctx.get_guild(payload.guild_id)
    quotes_channel = await guild.fetch_channel(quotes_channel_id)

    channel = await guild.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    embed_of_message_quoted = await create_discord_embed(
        color=discord.Color(int(color,16)),
        title=message.author.display_name,
        description=message.content,
        date=message.created_at,
        author=responses_dict['origine'].format(user=payload.member.display_name),
        icon=payload.member.avatar.url,
        fields=[
            ("", payload.member.mention),
            ("", message.author.mention),
        ],
        thumbnail_url=message.author.avatar.url,
        footer_text=responses_dict['embed_footer']
    )

    await quotes_channel.send(embed=embed_of_message_quoted)
    await send_response_to_discord(ctx=message, content=responses_dict['response'])


# ██████╗ ███████╗███████╗██╗   ██╗██╗  ████████╗
# ██╔══██╗██╔════╝██╔════╝██║   ██║██║  ╚══██╔══╝
# ██████╔╝█████╗  ███████╗██║   ██║██║     ██║
# ██╔══██╗██╔══╝  ╚════██║██║   ██║██║     ██║
# ██║  ██║███████╗███████║╚██████╔╝███████╗██║
# ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚══════╝╚═╝


async def _get_messages_of_month(channel: discord.TextChannel) -> list[discord.Message]:
    """Get all messages quoted during the last month"""
    end_date = datetime.now()
    start_date = end_date - relativedelta(months=1)

    messages = []

    async for message in channel.history(after=start_date, before=end_date):
        messages.append(message)

    return messages


async def _get_result(channel: discord.TextChannel):
    """Get the quoted message with the most reaction"""
    quoted_messages = await _get_messages_of_month(channel)

    top_message = max(
        quoted_messages,
        key=lambda m: sum(reaction.count for reaction in m.reactions)
    )

    return top_message


async def reset_quote(ctx: commands.Bot):
    """
    Send a message during the first day of the month in the quote channel,
    and annonce the winner message

    Parameters:
        ctx (commands.Bot): The bot instance
    """
    guild = ctx.get_guild(BOT['guild_dev'])
    quotes_channel_id = BOT['channels']['quotes']
    channel = await guild.fetch_channel(quotes_channel_id)

    splitter1 = await create_discord_file(filename="bot/assets/splitter.png")
    await channel.send(file=splitter1)

    # --- Send result ---

    result = await _get_result(channel)

    embed = result.embeds[0]
    discloser_user = embed.fields[0].value
    author_user = embed.fields[1].value

    response = STRINGS['fun']['quote_component']['month_result'].format(
        month=datetime.now().strftime("%B"),
        discloser=discloser_user,
        author=author_user
    )

    result_message = await channel.send(content=response)
    await result_message.reply(embed=embed)

    splitter2 = await create_discord_file(filename="bot/assets/splitter.png")
    await channel.send(file=splitter2)
