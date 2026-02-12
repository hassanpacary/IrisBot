"""
bot/cogs/fun.py
© by hassanpacary

Cog containing fun slash commands and their logic
"""

# --- Imports ---
import logging

# --- Third party imports ---
import discord
from discord import app_commands
from discord.ext import commands

# --- Bot modules ---
from bot.core.config_loader import COMMANDS
from bot.services.social.social_service import display_profile, choose_color, retrieve_user_avatar


# ███████╗ ██████╗  ██████╗██╗ █████╗ ██╗
# ██╔════╝██╔═══██╗██╔════╝██║██╔══██╗██║
# ███████╗██║   ██║██║     ██║███████║██║
# ╚════██║██║   ██║██║     ██║██╔══██║██║
# ███████║╚██████╔╝╚██████╗██║██║  ██║███████╗
# ╚══════╝ ╚═════╝  ╚═════╝╚═╝╚═╝  ╚═╝╚══════╝


class SocialCog(commands.Cog):
    """Fun cog class"""

    def __init__(self, bot):
        """Initialize the cog with a reference to the bot."""
        self.bot = bot

    #  ██████╗ ██████╗ ███╗   ███╗███╗   ███╗ █████╗ ███╗   ██╗██████╗ ███████╗
    # ██╔════╝██╔═══██╗████╗ ████║████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝
    # ██║     ██║   ██║██╔████╔██║██╔████╔██║███████║██╔██╗ ██║██║  ██║███████╗
    # ██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║  ██║╚════██║
    # ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║██████╔╝███████║
    #  ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝

    @app_commands.command(
        name=COMMANDS['social']['avatar']['slash_command'],
        description=COMMANDS['social']['avatar']['description'],
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def avatar_logic(self, interaction: discord.Interaction, user: discord.User):
        """
        Responds to the /avatar slash command

        Parameters:
            interaction (discord.Interaction): The interaction object triggered by the user
            user (discord.User): Utilisateur cible

        Action:
            - Reply to the user with avatar image
        """
        logging.info(
            "-- %s use /avatar slash command for retrieving %s avatar",
            interaction.user.name,
            user.name
        )
        await retrieve_user_avatar(ctx=interaction, user=user)

    @app_commands.command(
        name=COMMANDS['social']['mycolor']['slash_command'],
        description=COMMANDS['social']['mycolor']['description'],
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def mycolor_logic(self, interaction: discord.Interaction, name:str, color: str):
        """
        Responds to the /mycolor slash command

        Parameters:
            interaction (discord.Interaction): The interaction object triggered by the user.
            name (str): Nom du rôle
            color (str): Couleur du rôle

        Action:
            - Create a new role with a custom color for the user
        """
        logging.info(
            "-- %s use /color slash command",
            interaction.user.name
        )

        await choose_color(
            ctx=interaction,
            color_db=self.bot.color_db,
            level_db=self.bot.level_db,
            role_name=name,
            hex_value=color
        )

    @app_commands.command(
        name=COMMANDS['social']['profile']['slash_command'],
        description=COMMANDS['social']['profile']['description'],
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def profile_logic(self, interaction: discord.Interaction, user: discord.User = None):
        """
        Responds to the /profile slash command

        Parameters:
            interaction (discord.Interaction): The interaction object triggered by the user
            user (discord.User): Utilisateur cible (par défaut vous)

        Action:
            - Display user profil card
        """
        logging.info(
            "-- %s use /profile slash command",
            interaction.user.name
        )

        await display_profile(ctx=interaction, db=self.bot.level_db, user=user)


async def setup(bot):
    """Adds this cog to the given bot"""
    await bot.add_cog(SocialCog(bot))
