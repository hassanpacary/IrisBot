"""
bot/services/guild_service.py
© by hassanpacary

Utility functions for multiples guild functions
"""

# --- Imports ---
import random

# --- Third party imports ---
import discord

# --- Bot modules ---
from bot.core.config_loader import BOT, STRINGS
from bot.utils.discord_utils import send_message_in_channel


# pylint: disable=line-too-long
#  ██████╗ ██╗   ██╗██╗██╗     ██████╗     ███████╗███████╗██████╗ ██╗   ██╗██╗ ██████╗███████╗███████╗
# ██╔════╝ ██║   ██║██║██║     ██╔══██╗    ██╔════╝██╔════╝██╔══██╗██║   ██║██║██╔════╝██╔════╝██╔════╝
# ██║  ███╗██║   ██║██║██║     ██║  ██║    ███████╗█████╗  ██████╔╝██║   ██║██║██║     █████╗  ███████╗
# ██║   ██║██║   ██║██║██║     ██║  ██║    ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██║██║     ██╔══╝  ╚════██║
# ╚██████╔╝╚██████╔╝██║███████╗██████╔╝    ███████║███████╗██║  ██║ ╚████╔╝ ██║╚██████╗███████╗███████║
#  ╚═════╝  ╚═════╝ ╚═╝╚══════╝╚═════╝     ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚═╝ ╚═════╝╚══════╝╚══════╝
# pylint: enable=line-too-long


async def welcome_new_member(member: discord.Member):
    """Welcoming a new member"""
    channel_id = BOT['channels']['welcome']
    message = random.choice(
        STRINGS['guild']['event_component']['welcome_member'].format(member=member.mention)
    )

    await send_message_in_channel(
        ctx=member,
        channel_id=channel_id,
        content=message
    )


async def goodbye_former_member(member: discord.Member):
    """Goodbye to a former member"""
    channel_id = BOT['channels']['goodbye']
    message = random.choice(
        STRINGS['guild']['event_component']['goodbye_member'].format(member=member.mention)
    )

    await send_message_in_channel(
        ctx=member,
        channel_id=channel_id,
        content=message
    )
