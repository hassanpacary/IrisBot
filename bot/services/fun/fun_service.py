"""
bot/services/fun/fun_service.py
© by hassanpacary

Utility functions for general fun cog
"""

# --- Imports ---
import random

# --- Third party imports ---
import discord

# --- Bot modules ---
from bot.core.config_loader import STRINGS
from bot.utils.discord_utils import send_response_to_discord


# ██████╗  ██████╗ ██╗     ██╗
# ██╔══██╗██╔═══██╗██║     ██║
# ██████╔╝██║   ██║██║     ██║
# ██╔══██╗██║   ██║██║     ██║
# ██║  ██║╚██████╔╝███████╗███████╗
# ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝


async def roll_dice(ctx: discord.Interaction, sides: int):
    """Logic of /roll command"""
    random_number_1 = random.randint(1, sides)
    random_number_2 = random_number_1
    response = STRINGS['fun']['roll_result'].format(
        first_result=random_number_1,
        second_result=random_number_2
    )

    # As long as random_number_1 is equal to random_number_2, we rethrow it
    while random_number_1 == random_number_2:
        random_number_2 = random.randint(1, sides)

    await send_response_to_discord(
        ctx=ctx,
        content=response,
    )


# ███████╗ █████╗ ██╗   ██╗
# ██╔════╝██╔══██╗╚██╗ ██╔╝
# ███████╗███████║ ╚████╔╝
# ╚════██║██╔══██║  ╚██╔╝
# ███████║██║  ██║   ██║
# ╚══════╝╚═╝  ╚═╝   ╚═╝


async def repeat_message(ctx: discord.Interaction, message: str):
    """Logic of /say command"""
    random_swap = random.randint(0, 1)

    await send_response_to_discord(ctx=ctx, content=message, detach=True)

    if random_swap:
        response = (
            STRINGS['fun']['say_component']['repeat_with_success_sus'].format(
                user=ctx.user.mention
            )
        )
        await send_response_to_discord(
            ctx=ctx,
            content=response
        )
    else:
        response = STRINGS['fun']['say_component']['repeat_with_success']
        await send_response_to_discord(
            ctx=ctx,
            content=response,
            ephemeral=True
        )
