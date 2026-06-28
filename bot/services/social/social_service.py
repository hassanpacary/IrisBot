"""Social service for social cog.

Manage logics functions for display user avatar command.

© by hassanpacary
"""

# --- Standard library ---
import logging

# --- Third-party ---
import discord

# --- Internal ---
from bot.cogs.social import social_strings
from bot.config import colors_config
from bot.utils import discord_utils


async def retrieve_avatar(
        interaction: discord.Interaction,
        user: discord.User,
) -> None:
    """Sends an embed displaying the target user's avatar.

    Args:
        interaction: The Discord interaction context.
        user: The Discord user whose avatar will be displayed.
    """
    embed = await discord_utils.create_discord_embed(
        color=discord.Color(int(colors_config.ORANGE, 16)),
        author=social_strings.AvatarEmbedFields.AUTHOR.format(user=user.name),
        icon=discord_utils.get_guild_icon(bot=None, guild=interaction.guild),
        image_url=str(user.display_avatar.url),
    )

    await interaction.response.send_message(embed=embed)

    logging.info(
        "%s retrieved avatar for %s",
        interaction.user.name,
        user.name,
    )
