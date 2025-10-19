"""
bot/services/guild/modal_factory.py
© by hassanpacary

Factor UI modal
"""

# --- Third party imports ---
import discord
from discord import ui

# --- Bot modules ---
from bot.core.config_loader import STRINGS
from bot.utils.discord_utils import send_response_to_discord


# ███╗   ███╗ ██████╗ ██████╗  █████╗ ██╗
# ████╗ ████║██╔═══██╗██╔══██╗██╔══██╗██║
# ██╔████╔██║██║   ██║██║  ██║███████║██║
# ██║╚██╔╝██║██║   ██║██║  ██║██╔══██║██║
# ██║ ╚═╝ ██║╚██████╔╝██████╔╝██║  ██║███████╗
# ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝


class MessageModal(ui.Modal, title='Questionnaire Response'):
    """Modal class"""

    # Message item in modal pop-up
    message = ui.Label(
        text=STRINGS['guild']['modal_factory']['label_text'],
        component=ui.TextInput(
            placeholder=STRINGS['guild']['modal_factory']['placeholder'],
            style=discord.TextStyle.paragraph, # type: ignore
            required=True,
        )
    )

    async def on_submit(self, interaction: discord.Interaction):
        """
        Callback for modal submit. call when /send command is use

        Parameters:
            interaction (discord.Interaction): Interaction object
        """
        await send_response_to_discord(
            ctx=interaction,
            content=STRINGS['guild']['modal_factory']['interaction_response'],
            ephemeral=True
        )

        await send_response_to_discord(
            ctx=interaction,
            content=self.message.component.value, # type: ignore
            detach=True
        )
