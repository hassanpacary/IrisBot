"""
vocal.py
© by hassanpacary

Cog containing vocal slash commands for the bot.
"""
import logging

# --- Imports ---
import discord
from discord import app_commands
from discord.ext import commands

# --- Bot modules ---
from bot.core.config_loader import BOT, COMMANDS, STRINGS
from bot.services.azure_service import text_to_speech
from bot.utils.discord_utils import send_response_to_discord


#  ██████╗██╗  ██╗ █████╗ ████████╗██████╗  ██████╗ ████████╗
# ██╔════╝██║  ██║██╔══██╗╚══██╔══╝██╔══██╗██╔═══██╗╚══██╔══╝
# ██║     ███████║███████║   ██║   ██████╔╝██║   ██║   ██║
# ██║     ██╔══██║██╔══██║   ██║   ██╔══██╗██║   ██║   ██║
# ╚██████╗██║  ██║██║  ██║   ██║   ██████╔╝╚██████╔╝   ██║
#  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═════╝  ╚═════╝    ╚═╝


class VocalCog(commands.Cog):
    """Cog containing vocal commands for the bot."""

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
            - Check if the message is sent in the vocal channel (textuel) and if Iris is in vocal
                - If matched, calls text_to_speech for TTS
            - Other messages are ignored by this listener.
        """
        vocal_text_id = BOT['channels']['textuel_vocal_channel']

        # --- Ignore bot message ---
        if message.author == self.bot.user:
            return

        message_author_voice_state = message.author.voice
        bot_voice_client = discord.utils.get(self.bot.voice_clients, guild=message.guild)

        # --- Text to speech event listener ---
        if (message_author_voice_state and
                bot_voice_client and
                message_author_voice_state.channel == bot_voice_client.channel and
                message.channel.id == vocal_text_id):
            await text_to_speech(bot_voice_client, message=message)
            logging.info(f"-- {message.author} send {message.content} and was played by the bot in vocal channel")

        await self.bot.process_commands(message)

    #  ██████╗ ██████╗ ███╗   ███╗███╗   ███╗ █████╗ ███╗   ██╗██████╗ ███████╗    ██╗      ██████╗  ██████╗ ██╗ ██████╗
    # ██╔════╝██╔═══██╗████╗ ████║████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝    ██║     ██╔═══██╗██╔════╝ ██║██╔════╝
    # ██║     ██║   ██║██╔████╔██║██╔████╔██║███████║██╔██╗ ██║██║  ██║███████╗    ██║     ██║   ██║██║  ███╗██║██║
    # ██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║  ██║╚════██║    ██║     ██║   ██║██║   ██║██║██║
    # ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║██████╔╝███████║    ███████╗╚██████╔╝╚██████╔╝██║╚██████╗
    #  ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝    ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝ ╚═════╝

    @app_commands.command(
        name=COMMANDS['vocal']['join']['slash_command'],
        description=COMMANDS['vocal']['join']['description'],
    )
    async def join_logic(self, interaction: discord.Interaction):
        """
        Command for making Iris join the user's voice channel.

        Event:
            Triggered when a user executes the /join command.

        Action:
            - Checks if the user is connected to a voice channel.
            - If the user is not in a voice channel, sends an ephemeral warning message.
            - If the bot is already connected to the same channel, sends an ephemeral
              confirmation that it is already present.
            - If the bot is connected to a different voice channel, it moves the bot
              to the user's channel and confirms the change.
            - If the bot is not connected, it joins the user's voice channel and
              confirms a successful connection.
        """
        responses_strings = STRINGS['vocal']

        user = interaction.user
        bot_voice_client = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)

        # --- User is not connected in vocal channel ---
        if not user.voice or not user.voice.channel:
            await send_response_to_discord(
                target=interaction,
                content=responses_strings['user_not_connected'],
                ephemeral=True
            )
            return

        # --- Bot is already connected in vocal channel ---
        if bot_voice_client is not None and bot_voice_client.channel == user.voice.channel:
            await send_response_to_discord(
                target=interaction,
                content=responses_strings['bot_already_connected'],
                ephemeral=True
            )
            return

        # --- Bot is not in the same vocal channel of the user ---
        if bot_voice_client is not None and bot_voice_client.channel != user.voice.channel:
            await send_response_to_discord(
                target=interaction,
                content=responses_strings['bot_change_channel'],
                ephemeral=True
            )
            await bot_voice_client.move_to(user.voice.channel)
            logging.info(f"-- {interaction.message.author} use /join slash command. The bot has changed channel")
            return

        # --- Else connect the bot in same vocal channel as the user
        await send_response_to_discord(
            target=interaction,
            content=responses_strings['bot_connect_with_success'],
            ephemeral=True
        )
        await user.voice.channel.connect()
        logging.info(f"-- {interaction.message.author} use /join slash command. The bot connect to channel")

    @app_commands.command(
        name=COMMANDS['vocal']['disconnect']['slash_command'],
        description=COMMANDS['vocal']['disconnect']['description'],
    )
    async def disconnect_logic(self, interaction: discord.Interaction):
        """
        Command for making Iris disconnect from the voice channel.

        Event:
            Triggered when a user executes the /disconnect command.

        Action:
            - Checks if the bot is connected to a voice channel in the guild.
            - If the bot is not connected, sends an ephemeral warning message.
            - If the bot is connected, disconnects from the voice channel and
              sends an ephemeral confirmation message.
        """
        responses_strings = STRINGS['vocal']

        voice_client = interaction.guild.voice_client

        # --- Bot is not connected ---
        if not voice_client or not voice_client.is_connected():  # type: ignore
            await send_response_to_discord(
                target=interaction,
                content=responses_strings['bot_is_not_connected'],
                ephemeral=True
            )
            return

        # --- Else disconnect the bot ---
        await send_response_to_discord(
            target=interaction,
            content=responses_strings['bot_disconnected_with_success'],
            ephemeral=True
        )
        await voice_client.disconnect(force=True)
        logging.info(f"-- {interaction.message.author} use /disconnect slash command. the bot has disconnected from channel")


async def setup(bot):
    """
    Adds this cog to the given bot.

    Args:
        bot (commands.Bot): The bot instance to which the cog will be added.
    """
    await bot.add_cog(VocalCog(bot))
