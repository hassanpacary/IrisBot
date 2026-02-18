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
from bot.core.config_loader import STRINGS, BOT, REGEX
from bot.utils.db_manager import DatabaseManager
from bot.utils.discord_utils import send_response_to_discord, create_discord_embed
from bot.utils.strings_utils import matches_pattern


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


#  ██████╗ ██████╗ ██╗      ██████╗ ██████╗
# ██╔════╝██╔═══██╗██║     ██╔═══██╗██╔══██╗
# ██║     ██║   ██║██║     ██║   ██║██████╔╝
# ██║     ██║   ██║██║     ██║   ██║██╔══██╗
# ╚██████╗╚██████╔╝███████╗╚██████╔╝██║  ██║
#  ╚═════╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝


async def _create_color_role(
        ctx: discord.Interaction,
        db: DatabaseManager,
        role_name: str,
        hex_value: str
):
    """
    Create and assign color role to the user

    Parameters:
        ctx (discord.Interaction): The interaction object triggered by the user
        db (DatabaseManager): DatabaseManager
        role_name (str): Created role name
        hex_value (str): Hexadecimal code of the color
    """
    if hex_value.startswith('#'):
        color = discord.Color.from_str(hex_value)
    else:
        color = discord.Color(int(hex_value, 16))

    created_role = await ctx.guild.create_role(
        name=role_name,
        color=color
    )

    await created_role.edit(position=ctx.guild.get_role(BOT['social']['color_role_id_position']).position - 1)

    user_id = ctx.user.id
    color_db = await db.fetchall("fetch_all", user_id)

    if not color_db:
        await db.execute("insert_color", user_id, created_role.id)
    else:
        role_id = color_db[0][1]
        await ctx.guild.get_role(role_id).delete(reason=STRINGS['social']['mycolor']['mycolor_delete_reason'])

        await db.execute("update_color", created_role.id, user_id)

    await ctx.user.add_roles(created_role, reason=STRINGS['social']['mycolor']['mycolor_create_reason'])

async def choose_color(
        ctx: discord.Interaction,
        color_db: DatabaseManager,
        level_db: DatabaseManager,
        role_name: str,
        hex_value: str
):
    """Logic of /mycolor command"""
    pattern = REGEX['hex']['pattern']

    user_id = ctx.user.id
    user_db = await level_db.fetchall("fetch_all", user_id)
    user_lvl = user_db[0][2]

    if user_lvl >= BOT['social']['level_for_color']:
        if matches_pattern(pattern, hex_value):
            await _create_color_role(
                ctx=ctx,
                db=color_db,
                role_name=role_name,
                hex_value=hex_value
            )

            await send_response_to_discord(
                ctx=ctx,
                content=STRINGS['social']['mycolor']['mycolor_color_created'],
                ephemeral=True
            )
        else:
            await send_response_to_discord(
                ctx=ctx,
                content=STRINGS['social']['mycolor']['mycolor_hexa_not_matched'],
                ephemeral=True
            )
    else:
        await send_response_to_discord(
            ctx=ctx,
            content=STRINGS['social']['mycolor']['mycolor_lvl_not_reached'],
            ephemeral=True
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
        user (discord.User): the discord user
        user_data (dict): the user data (contains: xp, level and next_level)
    """
    color = "#" + BOT['color']['social']

    harmony_font = Font(path="bot/assets/fonts/harmonyos_sans_black.ttf", size=20)
    harmony_font_italic = Font(path="bot/assets/fonts/harmonyos_sans_black_italic.ttf", size=90)

    # User data
    card_template = Editor("bot/assets/card_template.png").image
    user_avatar_img = await load_image_async(str(user.avatar.url))
    user_name = user.display_name.upper()
    user_xp = user_data['xp']
    user_level = user_data['level']
    user_next_level = user_data['next_level']

    # Card editor
    card = Editor(Canvas((900, 300), color=color))
    card.paste(card_template, (0, 0))

    user_avatar = Editor(user_avatar_img).resize((360, 360)).rounded_corners(50, 50)
    card.paste(user_avatar, (550, -30))

    card.text((40, 70), user_name, font=harmony_font_italic, color="#FCCD71")
    card.text((40, 40), user_name, font=harmony_font_italic, color="#FFFFFF")
    card.text(
        (40, 245),
        f"L     E     V     E     L        {user_level}",
        font=harmony_font,
        color="#FFFFFF"
    )
    card.text(
        (480, 245),
        f"{user_xp} / {user_next_level}",
        font=harmony_font,
        color="#FFFFFF"
    )

    card.bar((35, 210), max_width=550, height=25, percentage=user_xp, color=color, radius=20)

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
