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
from bot.core.config_loader import BOT, COMMANDS, STRINGS
from bot.utils.discord_utils import send_response_to_discord


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

    #  ██████╗ ██████╗ ███╗   ███╗███╗   ███╗ █████╗ ███╗   ██╗██████╗ ███████╗    ██╗      ██████╗  ██████╗ ██╗ ██████╗
    # ██╔════╝██╔═══██╗████╗ ████║████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝    ██║     ██╔═══██╗██╔════╝ ██║██╔════╝
    # ██║     ██║   ██║██╔████╔██║██╔████╔██║███████║██╔██╗ ██║██║  ██║███████╗    ██║     ██║   ██║██║  ███╗██║██║
    # ██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║  ██║╚════██║    ██║     ██║   ██║██║   ██║██║██║
    # ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║██████╔╝███████║    ███████╗╚██████╔╝╚██████╔╝██║╚██████╗
    #  ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝    ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝ ╚═════╝

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
        logging.info(f"-- {interaction.user.name} use /purge slash command for delete {amount} messages in chat")

        amount_max = BOT['moderation']['purge_amount_max']
        responses = STRINGS['moderation']

        # --- Not manage_messages permission ---
        if not interaction.user.guild_permissions.manage_messages:
            await send_response_to_discord(
                target=interaction,
                content=responses['not_permission'],
                ephemeral=True
            )
            return

        # --- Messages amount is too high ---
        if amount > amount_max:
            await send_response_to_discord(
                target=interaction,
                content=responses['amount_too_high'].format(max=amount_max),
                ephemeral=True
            )

        # --- Purge chat ---
        else:
            await interaction.response.defer(ephemeral=True) # type: ignore

            await interaction.channel.purge(limit=amount)

            await send_response_to_discord(
                target=interaction,
                content=responses['purge_ok'].format(amount=str(amount)),
                ephemeral=True
            )


async def setup(bot):
    """Adds this cog to the given bot"""
    await bot.add_cog(ModerationCog(bot))
