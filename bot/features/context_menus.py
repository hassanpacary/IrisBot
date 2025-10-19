"""
bot/context_menu/context_menus.py
© by hassanpacary

Context menus containing application commands and their logic
"""

# -- Imports ---
import logging

# --- Third party imports ---
import discord
from discord import app_commands

# --- Bot modules ---
from bot.core.config_loader import COMMANDS
from bot.services.fun.quote_component import quote_user_message


# pylint: disable=line-too-long
#  ██████╗ ██████╗ ███╗   ██╗████████╗███████╗██╗  ██╗████████╗    ███╗   ███╗███████╗███╗   ██╗██╗   ██╗
# ██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝██╔════╝╚██╗██╔╝╚══██╔══╝    ████╗ ████║██╔════╝████╗  ██║██║   ██║
# ██║     ██║   ██║██╔██╗ ██║   ██║   █████╗   ╚███╔╝    ██║       ██╔████╔██║█████╗  ██╔██╗ ██║██║   ██║
# ██║     ██║   ██║██║╚██╗██║   ██║   ██╔══╝   ██╔██╗    ██║       ██║╚██╔╝██║██╔══╝  ██║╚██╗██║██║   ██║
# ╚██████╗╚██████╔╝██║ ╚████║   ██║   ███████╗██╔╝ ██╗   ██║       ██║ ╚═╝ ██║███████╗██║ ╚████║╚██████╔╝
#  ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝   ╚═╝       ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝
# pylint: enable=line-too-long


def setup(ctx):
    """Load all context_menus commands"""
    ctx.tree.add_command(quote_context)
    logging.info("-- Loaded quote_context command in context menu successfully")


@app_commands.context_menu(name=COMMANDS['fun']['quote']['context_menu'])
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def quote_context(interaction: discord.Interaction, message: discord.Message):
    """
    In response to the context menu command Quote

    Parameters:
        interaction (discord.Interaction): The interaction object triggered by the user
        message (discord.Message): The message to quote

    Action:
        - Quote the message in the quotes channel for pins it
    """
    logging.info("-- New quoted user from context menu")
    await quote_user_message(interaction, message)
