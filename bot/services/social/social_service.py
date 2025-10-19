"""
bot/services/fun/fun_service.py
© by hassanpacary

Utility functions for general fun cog
"""

# --- Imports ---
import io

# --- Third party imports ---
import discord
from easy_pil import *

# --- Bot modules ---
from bot.core.config_loader import STRINGS, BOT
from bot.utils.db_manager import DatabaseManager
from bot.utils.discord_utils import send_response_to_discord, create_discord_embed


#  █████╗ ██╗   ██╗ █████╗ ████████╗ █████╗ ██████╗
# ██╔══██╗██║   ██║██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗
# ███████║██║   ██║███████║   ██║   ███████║██████╔╝
# ██╔══██║╚██╗ ██╔╝██╔══██║   ██║   ██╔══██║██╔══██╗
# ██║  ██║ ╚████╔╝ ██║  ██║   ██║   ██║  ██║██║  ██║
# ╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝


async def retrieve_user_avatar(ctx: discord.Interaction, user: discord.User):
    """Logic of /avatar command"""
    color = BOT['color']['social']
    avatar_embed = await create_discord_embed(
        color=discord.Color(int(color, 16)),
        author=STRINGS['social']['avatar_component']['embed_author_field'].format(user=user.name),
        icon=ctx.guild.icon.url,
        image_url=user.display_avatar.url
    )

    await send_response_to_discord(
        ctx=ctx,
        content=STRINGS['social']['avatar_component']['retrieve'].format(user=user.mention),
        embed=avatar_embed
    )


#  ██████╗ █████╗ ██████╗ ██████╗
# ██╔════╝██╔══██╗██╔══██╗██╔══██╗
# ██║     ███████║██████╔╝██║  ██║
# ██║     ██╔══██║██╔══██╗██║  ██║
# ╚██████╗██║  ██║██║  ██║██████╔╝
#  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝


async def _create_user_card(user: discord.User, user_data: dict) -> io.BytesIO:
    """
    Create the card containing all user information

    Parameters:
        - user (discord.User): the discord user
        - user_data (dict): the user data (contains: xp, level and next_level)
    """
    color = "#" + BOT['color']['social']
    card = Editor(Canvas((900, 300), color=color))

    profile_picture = await load_image_async(str(user.avatar.url))
    profile = Editor(profile_picture).resize((150, 150)).circle_image()

    poppins = Font.poppins(size=40)
    poppins_small = Font.poppins(size=30)

    card_right_shape = [(600, 0), (750, 300), (900, 300), (900, 0)]

    card.polygon(card_right_shape, "#FFFFFF")
    card.paste(profile, (30, 30))

    card.rectangle((30, 220), width=650, height=40, color="#FFFFFF", radius=20)
    card.bar((30, 215), max_width=650, height=50, percentage=user_data['xp'], color="#282828", radius=20)
    card.text((200, 40), user.display_name, font=poppins, color="#FFFFFF")

    card.rectangle((200, 100), width=350, height=2, fill="#FFFFFF")
    card.text(
        (200, 100),
        f"Level - {user_data['level']} | XP - {user_data['xp']}/{user_data['next_level']}",
        font=poppins_small,
        color="#FFFFFF"
    )

    return card.image_bytes


async def display_profile(ctx: discord.Interaction, db: DatabaseManager, user: discord.User):
    """logic of /level command"""
    response = STRINGS['social']['no_profile']

    if user is not None:
        user_id = user.id
    else:
        user = ctx.user
        user_id = ctx.user.id

    user_db = await db.fetchall("fetch_all", user_id)

    if user_db is None:
        await send_response_to_discord(
            ctx=ctx,
            content=response,
            ephemeral=True
        )

    user_data = {
        'xp': user_db[0][1],
        'level': user_db[0][2],
        'next_level': user_db[0][3]
    }

    user_card_bytes = await _create_user_card(user=user, user_data=user_data)
    user_card = discord.File(fp=user_card_bytes, filename="user_card.png")

    await send_response_to_discord(
        ctx=ctx,
        files=[user_card]
    )
