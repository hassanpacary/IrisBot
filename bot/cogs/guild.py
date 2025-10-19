"""
bot/cogs/bot.py
© by hassanpacary

Cog containing globals events listener and their logic
"""

# --- Imports ---
import logging

# --- Third party imports ---
import discord
from discord import app_commands
from discord.ext import commands

# --- bot modules ---
from bot.core.config_loader import ON_READY_BANNER, COMMANDS, STRINGS
from bot.features import context_menus
from bot.features.tasks import TasksScheduler
from bot.services.guild.cogs_factory import load_cogs, reload_cogs, unload_cogs
from bot.services.guild.guild_service import welcome_new_member, goodbye_former_member
from bot.services.guild.modal_factory import MessageModal
from bot.utils.discord_utils import send_response_to_discord


# pylint: disable=line-too-long
#  ██████╗ ██╗      ██████╗ ██████╗  █████╗ ██╗         ███████╗██╗   ██╗███████╗███╗   ██╗████████╗███████╗
# ██╔════╝ ██║     ██╔═══██╗██╔══██╗██╔══██╗██║         ██╔════╝██║   ██║██╔════╝████╗  ██║╚══██╔══╝██╔════╝
# ██║  ███╗██║     ██║   ██║██████╔╝███████║██║         █████╗  ██║   ██║█████╗  ██╔██╗ ██║   ██║   ███████╗
# ██║   ██║██║     ██║   ██║██╔══██╗██╔══██║██║         ██╔══╝  ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║   ██║   ╚════██║
# ╚██████╔╝███████╗╚██████╔╝██████╔╝██║  ██║███████╗    ███████╗ ╚████╔╝ ███████╗██║ ╚████║   ██║   ███████║
#  ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝    ╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝
# pylint: enable=line-too-long


class GuildCog(commands.Cog):
    """Event cog class"""

    def __init__(self, bot):
        """Initialize the cog with a reference to the bot"""
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Event triggered when the bot is ready and connected to Discord"""
        banner = ON_READY_BANNER

        logging.info(banner)
        logging.info(
            "-- Bot connected as %s",
            self.bot.user.name
        )

        # Connect to level db
        await self.bot.level_db.connect()
        self.bot.level_db.load_queries("level.sql")
        await self.bot.level_db.execute("create_table_levels")

        # Start background tasks
        scheduler = TasksScheduler(self.bot)
        scheduler.start()

        # Setup context menus commands
        context_menus.setup(ctx=self.bot)

    @commands.Cog.listener()
    async def on_resumed(self):
        """Event listener triggered when the bot successfully reconnects"""
        logging.info(
            "-- Bot is resumed as %s",
            self.bot.user.name
        )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """
        Event triggered when a new member joins the server

        Parameters:
            member (discord.Member): The member who joined the server

        Action:
            Sends a welcome message in the server's system channel
        """
        logging.info(
            "-- New member joined %s",
            member.name
        )
        await welcome_new_member(member=member)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """
        Event triggered when a member leave the server

        Parameters:
            member (discord.Member): The member who left the server

        Action:
            Sends a leave message in the server's system channel
        """
        logging.info(
            "-- member leave server %s",
            member.name
        )
        await goodbye_former_member(member=member)

    #  ██████╗ ██████╗ ███╗   ███╗███╗   ███╗ █████╗ ███╗   ██╗██████╗ ███████╗
    # ██╔════╝██╔═══██╗████╗ ████║████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝
    # ██║     ██║   ██║██╔████╔██║██╔████╔██║███████║██╔██╗ ██║██║  ██║███████╗
    # ██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║  ██║╚════██║
    # ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║██████╔╝███████║
    #  ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝

    @app_commands.command(
        name=COMMANDS['guild']['load']['slash_command'],
        description=COMMANDS['guild']['load']['description'],
    )
    @app_commands.allowed_contexts(guilds=True)
    @app_commands.default_permissions(administrator=True)
    async def load_logic(self, interaction: discord.Interaction):
        """
        Responds to the /load slash command

        Parameters:
            interaction (discord.Interaction): The interaction object triggered by the user

        Action:
            - Load all cogs and command
        """
        response = STRINGS['guild']['cogs_factory']['load']

        logging.info(
            "-- %s use /load slash command",
            interaction.user.name
        )
        await send_response_to_discord(ctx=interaction, content=response, ephemeral=True)
        await load_cogs(ctx=self.bot)

    @app_commands.command(
        name=COMMANDS['guild']['reload']['slash_command'],
        description=COMMANDS['guild']['reload']['description'],
    )
    @app_commands.allowed_contexts(guilds=True)
    @app_commands.default_permissions(administrator=True)
    async def reload_logic(self, interaction: discord.Interaction):
        """
        Responds to the /reload slash command

        Parameters:
            interaction (discord.Interaction): The interaction object triggered by the user

        Action:
            - Reload all cogs and command
        """
        response = STRINGS['guild']['cogs_factory']['reload']

        logging.info(
            "-- %s use /reload slash command",
            interaction.user.name
        )
        await send_response_to_discord(ctx=interaction, content=response, ephemeral=True)
        await reload_cogs(ctx=self.bot)

    @app_commands.command(
        name=COMMANDS['guild']['send']['slash_command'],
        description=COMMANDS['guild']['send']['description'],
    )
    @app_commands.allowed_contexts(guilds=True)
    @app_commands.default_permissions(administrator=True)
    async def send_logic(self, interaction: discord.Interaction):
        """
        Responds to the /send slash command

        Parameters:
            interaction (discord.Interaction): The interaction object triggered by the user

        Action:
            - Open modal
            - Send message from the modal
        """
        logging.info(
            "-- %s use /send slash command",
            interaction.user.name
        )

        await interaction.response.send_modal(MessageModal())  # type: ignore

    @app_commands.command(
        name=COMMANDS['guild']['unload']['slash_command'],
        description=COMMANDS['guild']['unload']['description'],
    )
    @app_commands.allowed_contexts(guilds=True)
    @app_commands.default_permissions(administrator=True)
    async def unload_logic(self, interaction: discord.Interaction):
        """
        Responds to the /unload slash command

        Parameters:
            interaction (discord.Interaction): The interaction object triggered by the user

        Action:
            - Unload all cogs and command
        """
        response = STRINGS['guild']['cogs_factory']['unload']

        logging.info(
            "-- %s use /unload slash command",
            interaction.user.name
        )
        await send_response_to_discord(ctx=interaction, content=response, ephemeral=True)
        await unload_cogs(ctx=self.bot)


async def setup(bot):
    """Adds this cog to the given bot"""
    await bot.add_cog(GuildCog(bot))
