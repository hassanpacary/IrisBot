"""
bot/services/vocal/vocal_service.py
© by hassanpacary

Utility functions for bot vocal tasks
"""

# --- Third party imports ---
import discord

# --- Bot modules ---
from bot.core.config_loader import STRINGS
from bot.utils.discord_utils import send_response_to_discord


#      ██╗ ██████╗ ██╗███╗   ██╗    ██╗   ██╗ ██████╗  ██████╗ █████╗ ██╗
#      ██║██╔═══██╗██║████╗  ██║    ██║   ██║██╔═══██╗██╔════╝██╔══██╗██║
#      ██║██║   ██║██║██╔██╗ ██║    ██║   ██║██║   ██║██║     ███████║██║
# ██   ██║██║   ██║██║██║╚██╗██║    ╚██╗ ██╔╝██║   ██║██║     ██╔══██║██║
# ╚█████╔╝╚██████╔╝██║██║ ╚████║     ╚████╔╝ ╚██████╔╝╚██████╗██║  ██║███████╗
#  ╚════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝      ╚═══╝   ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝


async def join_channel(ctx: discord.Interaction, bot_voice: discord.VoiceClient):
    """Logic of /join command"""
    responses_dict = STRINGS['vocal']

    user = ctx.user

    # --- User is not connected in vocal channel ---
    if not user.voice or not user.voice.channel:
        await send_response_to_discord(
            ctx=ctx,
            content=responses_dict['user_not_connected'],
            ephemeral=True
        )
        return

    # --- Bot is already connected in vocal channel ---
    if bot_voice is not None and bot_voice.channel == user.voice.channel:
        await send_response_to_discord(
            ctx=ctx,
            content=responses_dict['already_connected'],
            ephemeral=True
        )
        return

    # --- Bot is not in the same vocal channel of the user ---
    if bot_voice is not None and bot_voice.channel != user.voice.channel:
        await send_response_to_discord(
            ctx=ctx,
            content=responses_dict['change_channel'],
            ephemeral=True
        )
        await bot_voice.move_to(user.voice.channel)
        return

    # --- Else connect the bot in same vocal channel as the user
    await send_response_to_discord(
        ctx=ctx,
        content=responses_dict['connect_with_success'],
        ephemeral=True
    )

    await user.voice.channel.connect()


# pylint: disable=line-too-long
# ██████╗ ██╗███████╗ ██████╗ ██████╗ ███╗   ██╗███╗   ██╗███████╗ ██████╗████████╗    ██╗   ██╗ ██████╗  ██████╗ █████╗ ██╗
# ██╔══██╗██║██╔════╝██╔════╝██╔═══██╗████╗  ██║████╗  ██║██╔════╝██╔════╝╚══██╔══╝    ██║   ██║██╔═══██╗██╔════╝██╔══██╗██║
# ██║  ██║██║███████╗██║     ██║   ██║██╔██╗ ██║██╔██╗ ██║█████╗  ██║        ██║       ██║   ██║██║   ██║██║     ███████║██║
# ██║  ██║██║╚════██║██║     ██║   ██║██║╚██╗██║██║╚██╗██║██╔══╝  ██║        ██║       ╚██╗ ██╔╝██║   ██║██║     ██╔══██║██║
# ██████╔╝██║███████║╚██████╗╚██████╔╝██║ ╚████║██║ ╚████║███████╗╚██████╗   ██║        ╚████╔╝ ╚██████╔╝╚██████╗██║  ██║███████╗
# ╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝ ╚═════╝   ╚═╝         ╚═══╝   ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝
# pylint: enable=line-too-long


async def disconnect_channel(ctx: discord.Interaction):
    """Logic of /join command"""
    responses_strings = STRINGS['vocal']

    voice_client = ctx.guild.voice_client

    # --- Bot is not connected ---
    if not voice_client or not voice_client.is_connected():  # type: ignore
        await send_response_to_discord(
            ctx=ctx,
            content=responses_strings['is_not_connected'],
            ephemeral=True
        )
        return

    # --- Else disconnect the bot ---
    await send_response_to_discord(
        ctx=ctx,
        content=responses_strings['disconnected_with_success'],
        ephemeral=True
    )

    await voice_client.disconnect(force=True)
