"""
bot/cogs/moderation.py
© by hassanpacary

Cog containing moderation slash commands and their logic
"""
import logging

# --- Third party imports ---
import discord
from discord import app_commands
from discord.ext import commands

# --- Bot modules ---
from bot.core.config_loader import COMMANDS
from bot.services.moderation.moderation_service import (
    log_deleted_message,
    log_edited_message,
    purge_messages)


# ██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██████╗     ███╗   ███╗ ██████╗ ██████╗
# ██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗    ████╗ ████║██╔═══██╗██╔══██╗
# ██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ██║    ██╔████╔██║██║   ██║██║  ██║
# ██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║    ██║╚██╔╝██║██║   ██║██║  ██║
# ██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║██████╔╝    ██║ ╚═╝ ██║╚██████╔╝██████╔╝
# ╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝     ╚═╝     ╚═╝ ╚═════╝ ╚═════╝


class ModerationCog(commands.Cog):
    """Moderation cog class"""

    def __init__(self, bot):
        """Initialize the cog with a reference to the bot."""
        self.bot = bot

    # ██╗      ██████╗  ██████╗
    # ██║     ██╔═══██╗██╔════╝
    # ██║     ██║   ██║██║  ███╗
    # ██║     ██║   ██║██║   ██║
    # ███████╗╚██████╔╝╚██████╔╝
    # ╚══════╝ ╚═════╝  ╚═════╝

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        """
        Event listener that triggers whenever a message is deleted

        Parameters:
            message (discord.Message): The message who trigger the listener

        Actions:
            - Log the deleted message
        """
        logging.info("-- a message has just been deleted")
        await log_deleted_message(ctx=self.bot, message=message)

    @commands.Cog.listener()
    async def on_message_edit(
            self,
            message_before: discord.Message,
            message_after: discord.Message
    ):
        """
        Event listener that triggers whenever a message is edited

        Parameters:
            message_before (discord.Message): The message before the edition
            message_after (discord.Message): The message after the edition

        Actions:
            - Log the edited message
        """
        logging.info("-- a message has just been edited")
        await log_edited_message(
            ctx=self.bot,
            message_before=message_before,
            message_after=message_after
        )

    # pylint: disable=line-too-long
    #  ██████╗ ██████╗ ███╗   ███╗███╗   ███╗ █████╗ ███╗   ██╗██████╗ ███████╗    ██╗      ██████╗  ██████╗ ██╗ ██████╗
    # ██╔════╝██╔═══██╗████╗ ████║████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝    ██║     ██╔═══██╗██╔════╝ ██║██╔════╝
    # ██║     ██║   ██║██╔████╔██║██╔████╔██║███████║██╔██╗ ██║██║  ██║███████╗    ██║     ██║   ██║██║  ███╗██║██║
    # ██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║  ██║╚════██║    ██║     ██║   ██║██║   ██║██║██║
    # ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║██████╔╝███████║    ███████╗╚██████╔╝╚██████╔╝██║╚██████╗
    #  ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝    ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝ ╚═════╝
    # pylint: enable=line-too-long

    @app_commands.command(
        name=COMMANDS['moderation']['purge']['slash_command'],
        description=COMMANDS['moderation']['purge']['description']
    )
    @app_commands.allowed_contexts(guilds=True)
    @app_commands.default_permissions(administrator=True)
    async def purge_logic(self, interaction: discord.Interaction, amount: int = 1):
        """
        Responds to the /purge slash command

        Action:
            - purge a certains amount of messages in chat
        """
        logging.info(
            "-- %s use /purge slash command for delete %s messages in chat",
            interaction.user.name,
            amount
        )
        await purge_messages(ctx=interaction, amount=amount)


async def setup(bot):
    """Adds this cog to the given bot"""
    await bot.add_cog(ModerationCog(bot))
