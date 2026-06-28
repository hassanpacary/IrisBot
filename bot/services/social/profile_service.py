"""Profile service for social cog.

Manage logics functions for displaying profile card. Generates a visual
profile card using easy_pil and sends it as a Discord file attachment.

© by hassanpacary
"""

# --- Standard library ---
import logging
from io import BytesIO

# --- Third-party ---
import discord
from easy_pil import Canvas, Editor, Font, load_image_async

# --- Internal ---
from bot.cogs.social import social_strings
from bot.config import assets_config, colors_config
from bot.utils import db_manager


async def _create_user_card(
        user: discord.User,
        user_data: dict,
) -> BytesIO:
    """Builds a profile card image for the given user.

    Args:
        user: The Discord user or member to generate the card for.
        user_data: A dict containing 'xp', 'level', and 'next_level'.

    Returns:
        The card image as bytes.
    """
    font = Font(path=assets_config.Font.FONT_PATH, size=20)
    font_italic = Font(path=assets_config.Font.FONT_ITALIC_PATH, size=90)

    card_template = Editor(assets_config.CARD_TEMPLATE_PATH)
    member_avatar_img = await load_image_async(str(user.display_avatar.url))
    member_name = user.display_name.upper()

    xp = user_data['xp']
    level = user_data['level']
    next_level = user_data['next_level']

    card = Editor(Canvas((900, 300), color=int(colors_config.ORANGE, 16)))
    card.paste(card_template, (0, 0))

    member_avatar = Editor(
        member_avatar_img,
    ).resize((360, 360)).rounded_corners(50, 50)
    card.paste(member_avatar, (550, -30))

    card.text(
        (40, 70),
        member_name,
        font=font_italic,
        color=f"#{colors_config.Utils.PROFILE_CARD_MEMBER_NAME}",
    )
    card.text(
        (40, 40),
        member_name,
        font=font_italic,
        color=f"#{colors_config.WHITE}",
    )
    card.text(
        (40, 245),
        social_strings.ProfileCard.LEVEL_LABEL.format(level=level),
        font=font,
        color=f"#{colors_config.WHITE}",
    )
    card.text(
        (480, 245),
        social_strings.ProfileCard.XP_LABEL.format(xp=xp, next_level=next_level),
        font=font,
        color=f"#{colors_config.WHITE}",
    )

    percentage = (xp / next_level) * 100
    card.bar((35, 210), max_width=550, height=25, percentage=percentage,
             color=f"#{colors_config.ORANGE}", radius=20)

    return card.image_bytes


async def display_profile(
        interaction: discord.Interaction,
        db: db_manager.DatabaseManager,
        user: discord.User,
) -> None:
    """Sends profile card for the target user.

    Replies with an ephemeral message if the user not figure in the database.

    Args:
        interaction: The Discord interaction context.
        db: The level database manager instance.
        user: The Discord user whose profile will be displayed.
    """
    user_db = await db.fetchall("fetch_all", user.id)

    if not user_db:
        await interaction.response.send_message(
            content=social_strings.ProfileCard.NO_PROFILE,
            ephemeral=True,
        )
        return

    user_data = {
        'xp': user_db[0][1],
        'level': user_db[0][2],
        'next_level': user_db[0][3],
    }

    card_bytes = await _create_user_card(user=user, user_data=user_data)
    card_file = discord.File(fp=card_bytes, filename="card.png")
    await interaction.response.send_message(file=card_file)

    logging.info(
        "%s requested profile for %s",
        interaction.user.name,
        user.name,
    )
