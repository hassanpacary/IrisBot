"""
bot/cogs/level.py
© by hassanpacary

Cog containing level slash commands and their logic
"""

# --- Imports ---
import logging

# --- Third party imports ---
import discord
from discord import app_commands
from discord.ext import commands

# --- Bot modules ---
from bot.core.config_loader import COMMANDS
from bot.services.level.level_service import get_leaderboard, update_xp_nd_level, reset_user_level


# ███████╗████████╗██╗███╗   ██╗ ██████╗██╗  ██╗██╗   ██╗
# ██╔════╝╚══██╔══╝██║████╗  ██║██╔════╝██║ ██╔╝╚██╗ ██╔╝
# ███████╗   ██║   ██║██╔██╗ ██║██║     █████╔╝  ╚████╔╝
# ╚════██║   ██║   ██║██║╚██╗██║██║     ██╔═██╗   ╚██╔╝
# ███████║   ██║   ██║██║ ╚████║╚██████╗██║  ██╗   ██║
# ╚══════╝   ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝   ╚═╝


class LevelCog(commands.Cog):
    """Level cog class"""

    def __init__(self, bot):
        """Initialize the cog with a reference to the bot"""
        self.bot = bot

    # ███████╗███████╗████████╗██╗   ██╗██████╗
    # ██╔════╝██╔════╝╚══██╔══╝██║   ██║██╔══██╗
    # ███████╗█████╗     ██║   ██║   ██║██████╔╝
    # ╚════██║██╔══╝     ██║   ██║   ██║██╔═══╝
    # ███████║███████╗   ██║   ╚██████╔╝██║
    # ╚══════╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Event triggered when a message is received from the server

        Parameters:
            message (discord.Message): The message who trigger the listener

        Actions:
            - Update level and xp for user
        """
        if message.author.bot:
            return

        await update_xp_nd_level(ctx=message, db=self.bot.level_db)

        await self.bot.process_commands(message)

    #  ██████╗ ██████╗ ███╗   ███╗███╗   ███╗ █████╗ ███╗   ██╗██████╗ ███████╗
    # ██╔════╝██╔═══██╗████╗ ████║████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝
    # ██║     ██║   ██║██╔████╔██║██╔████╔██║███████║██╔██╗ ██║██║  ██║███████╗
    # ██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║  ██║╚════██║
    # ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║██████╔╝███████║
    #  ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝

    @app_commands.command(
        name=COMMANDS['level']['givexp']['slash_command'],
        description=COMMANDS['level']['givexp']['description'],
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.default_permissions(administrator=True)
    async def givexp_logic(self, interaction: discord.Interaction, amount: int, user: discord.User):
        """
        Responds to the /givexp slash command

        Parameters:
            interaction (discord.Interaction): The interaction object triggered by the user
            amount (int): Nombre d'expérience à donner à l'utilisateur
            user (discord.User): Utilisateur cible

        Action:
            - Give xp to a target user
        """
        logging.info(
            "-- %s use /givexp slash command",
            interaction.user.name
        )
        await update_xp_nd_level(ctx=interaction, db=self.bot.level_db, amount=amount, target_user=user)

    @app_commands.command(
        name=COMMANDS['level']['leaderboard']['slash_command'],
        description=COMMANDS['level']['leaderboard']['description'],
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def leaderboard_logic(self, interaction: discord.Interaction):
        """
        Responds to the /leaderboard slash command

        Parameters:
            interaction (discord.Interaction): The interaction object triggered by the user

        Action:
            - Send the guild leaderboard of members level
        """
        logging.info(
            "-- %s use /leaderboard slash command",
            interaction.user.name
        )
        await get_leaderboard(ctx=interaction, db=self.bot.level_db)

    @app_commands.command(
        name=COMMANDS['level']['resetlvl']['slash_command'],
        description=COMMANDS['level']['resetlvl']['description'],
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.default_permissions(administrator=True)
    async def resetlvl_logic(self, interaction: discord.Interaction, user: discord.User):
        """
        Responds to the /resetlvl slash command

        Parameters:
            interaction (discord.Interaction): The interaction object triggered by the user
            user (discord.User): Utilisateur cible

        Action:
            - Reset XP and level for a user
        """
        logging.info(
            "-- %s use /reset slash command",
            interaction.user.name
        )

        await reset_user_level(ctx=interaction, db=self.bot.level_db, user=user)


async def setup(bot):
    """Adds this cog to the given bot"""
    await bot.add_cog(LevelCog(bot))
