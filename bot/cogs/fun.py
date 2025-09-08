"""
fun.py
© by hassanpacary

Cog containing fun slash commands logic.
"""

# --- Third party imports ---
import discord
from discord import app_commands
from discord.ext import commands

# --- Bot modules ---
from bot.services.response_service import send_response_to_discord
from bot.utils.strings_utils import matches_pattern


#  ██████╗██╗   ██╗███╗   ██╗███╗   ██╗██╗   ██╗
# ██╔════╝██║   ██║████╗  ██║████╗  ██║╚██╗ ██╔╝
# ██║     ██║   ██║██╔██╗ ██║██╔██╗ ██║ ╚████╔╝
# ██║     ██║   ██║██║╚██╗██║██║╚██╗██║  ╚██╔╝
# ╚██████╗╚██████╔╝██║ ╚████║██║ ╚████║   ██║
#  ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝   ╚═╝


class FunCog(commands.Cog):
    """Cog containing fun commands for the bot."""

    def __init__(self, bot):
        """Initialize the cog with a reference to the bot."""
        self.bot = bot

    # ███████╗██╗   ██╗███████╗███╗   ██╗████████╗███████╗    ██╗      ██████╗  ██████╗ ██╗ ██████╗
    # ██╔════╝██║   ██║██╔════╝████╗  ██║╚══██╔══╝██╔════╝    ██║     ██╔═══██╗██╔════╝ ██║██╔════╝
    # █████╗  ██║   ██║█████╗  ██╔██╗ ██║   ██║   ███████╗    ██║     ██║   ██║██║  ███╗██║██║
    # ██╔══╝  ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║   ██║   ╚════██║    ██║     ██║   ██║██║   ██║██║██║
    # ███████╗ ╚████╔╝ ███████╗██║ ╚████║   ██║   ███████║    ███████╗╚██████╔╝╚██████╔╝██║╚██████╗
    # ╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝    ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝ ╚═════╝

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        Event listener that triggers whenever a message is sent in a channel or DM.

        Action:
            - Ignores any message sent by the bot itself.
            - Checks if the message matches the "quoi-feur" pattern:
                - If matched, calls `reply_feur` to reply with the predefined response.
            - Other messages are ignored by this listener.
        """

        # --- Ignore bot message ---
        if message.author == self.bot.user:
            return

        # --- Message that contains 'quoi' listener ---
        pattern = self.bot.config['regex']['quoi']['pattern']

        if matches_pattern(pattern, message.content):
            await send_response_to_discord(target=message, content=self.bot.config['strings']['fun']['quoi'])

        await self.bot.process_commands(message)

    #  ██████╗ ██████╗ ███╗   ███╗███╗   ███╗ █████╗ ███╗   ██╗██████╗ ███████╗    ██╗      ██████╗  ██████╗ ██╗ ██████╗
    # ██╔════╝██╔═══██╗████╗ ████║████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝    ██║     ██╔═══██╗██╔════╝ ██║██╔════╝
    # ██║     ██║   ██║██╔████╔██║██╔████╔██║███████║██╔██╗ ██║██║  ██║███████╗    ██║     ██║   ██║██║  ███╗██║██║
    # ██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║  ██║╚════██║    ██║     ██║   ██║██║   ██║██║██║
    # ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║██████╔╝███████║    ███████╗╚██████╔╝╚██████╔╝██║╚██████╗
    #  ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝    ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝ ╚═════╝

    @app_commands.command(name="quoi", description="Répond 'feur' à quoi hihi.")
    async def quoi_logic(self, interaction: discord.Interaction):
        """
        Responds to the /quoi slash command.

        Args:
            interaction (discord.Interaction): The interaction object triggered by the user.

        Action:
            Sends the message stored in the QUOI variable to the user.
        """
        await send_response_to_discord(target=interaction, content=self.bot.config['strings']['fun']['quoi'])


async def setup(bot):
    """Adds this cog to the given bot."""
    await bot.add_cog(FunCog(bot))
