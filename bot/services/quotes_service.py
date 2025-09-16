"""
bot/services/quote_service.py
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
from bot.utils.discord_utils import create_discord_embed, send_response_to_discord, create_discord_file


#  ██████╗ ██╗   ██╗ ██████╗ ████████╗███████╗    ███████╗███████╗██████╗ ██╗   ██╗██╗ ██████╗███████╗
# ██╔═══██╗██║   ██║██╔═══██╗╚══██╔══╝██╔════╝    ██╔════╝██╔════╝██╔══██╗██║   ██║██║██╔════╝██╔════╝
# ██║   ██║██║   ██║██║   ██║   ██║   █████╗      ███████╗█████╗  ██████╔╝██║   ██║██║██║     █████╗
# ██║▄▄ ██║██║   ██║██║   ██║   ██║   ██╔══╝      ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██║██║     ██╔══╝
# ╚██████╔╝╚██████╔╝╚██████╔╝   ██║   ███████╗    ███████║███████╗██║  ██║ ╚████╔╝ ██║╚██████╗███████╗
#  ╚══▀▀═╝  ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝    ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚═╝ ╚═════╝╚══════╝


async def quote_user_message(interaction: discord.Interaction, message: discord.Message = None):
    """
    Quote a message in an embed message

    Parameters:
        interaction (discord.Interaction): The interaction with the user who issued the command
        message (discord.Message): The message to quote
    """
    strings = STRINGS['fun']

    guild = await interaction.client.fetch_guild(BOT['guild_dev'])
    quotes_channel_id = BOT['channels']['quotes_channel']
    channel = await guild.fetch_channel(quotes_channel_id)

    embed_of_message_quoted = await create_discord_embed(
        color=discord.Color(0xFDC830),
        title=message.author.display_name,
        description=message.content,
        date=message.created_at,
        author=strings['quote_origine'].format(user=interaction.user.display_name),
        icon=interaction.user.avatar.url,
        fields=[
            ("", interaction.user.mention),
            ("", message.author.mention),
        ],
        thumbnail_url=message.author.avatar.url,
        footer_text=strings['quote_embed_footer']
    )

    await channel.send(embed=embed_of_message_quoted)
    await send_response_to_discord(target=interaction, content=strings['quote_response'])


# ██████╗ ███████╗███████╗██╗   ██╗██╗  ████████╗
# ██╔══██╗██╔════╝██╔════╝██║   ██║██║  ╚══██╔══╝
# ██████╔╝█████╗  ███████╗██║   ██║██║     ██║
# ██╔══██╗██╔══╝  ╚════██║██║   ██║██║     ██║
# ██║  ██║███████╗███████║╚██████╔╝███████╗██║
# ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚══════╝╚═╝


async def _get_messages_of_month(channel: discord.TextChannel):
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


async def reset_quote(bot: commands.Bot):
    """
    Send a message during the first day of the month in the quote channel,
    and annonce the winner message

    Parameters:
        bot (commands.Bot): The bot instance
    """
    guild = bot.get_guild(BOT['guild_dev'])
    quotes_channel_id = BOT['channels']['quotes_channel']
    channel = await guild.fetch_channel(quotes_channel_id)

    splitter1 = create_discord_file(filename="bot/assets/splitter.png")
    await channel.send(file=splitter1)

    # --- Send result ---

    result = await _get_result(channel)

    embed = result.embeds[0]
    discloser_user = embed.fields[0].value
    author_user = embed.fields[1].value

    result_message = await channel.send(
        content=STRINGS['fun']['quote_month_result'].format(
            month=datetime.now().strftime("%B"),
            discloser=discloser_user,
            author=author_user,
        )
    )

    await result_message.reply(embed=embed)

    splitter2 = create_discord_file(filename="bot/assets/splitter.png")
    await channel.send(file=splitter2)
