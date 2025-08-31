"""
vocal_commands.py
© by hassanpacary

Cog containing vocal slash commands for the bot.

Commands:
- /join: Join vocal channel
- /disconnect: Disconnect vocal channel
"""

# --- Imports ---
import discord
from discord import app_commands
from discord.ext import commands

# --- Bot modules ---
from functions.functions import load_json

# Load config data from json files
config = load_json("config.json")
string = load_json(f"string_config_{config['config']['langage']}.json")


class VocalCommands(commands.Cog):
    """
    Cog containing vocal commands for the bot.

    Attributes:
        bot (commands.Bot): The main bot instance.
    """

    def __init__(self, bot):
        """
        Initialize the cog with a reference to the bot.

        Args:
            bot (commands.Bot): The bot instance.
        """
        self.bot = bot

    @app_commands.command(
        name=string['command']['join_vocal']['slash_command'],
        description=string['command']['join_vocal']['description']
    )
    @app_commands.guild_only()
    async def join(self, interaction: discord.Interaction):
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
        user = interaction.user
        bot_voice_client = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)

        # --- User is connected in vocal channel ---
        if not user.voice or not user.voice.channel:
            await interaction.response.send_message(
                string['vocal']['user_not_connected'],
                ephemeral=True
            )
            return

        # --- Bot is already connected in vocal channel ---
        if bot_voice_client is not None and bot_voice_client.channel == user.voice.channel:
            await interaction.response.send_message(
                string['vocal']['bot_already_connected'],
                ephemeral=True
            )
            return

        # --- Bot is not in the same vocal channel of the user ---
        if bot_voice_client is not None and bot_voice_client.channel != user.voice.channel:
            await interaction.response.send_message(
                string['vocal']['bot_change_channel'],
                ephemeral=True
            )
            await bot_voice_client.move_to(user.voice.channel)
            return

        # --- Else connect the bot in same vocal channel as the user
        await user.voice.channel.connect()
        await interaction.response.send_message(
            string['vocal']['bot_connect_with_success'],
            ephemeral=True
        )

        # This function processes the commands that have been registered to the bot.
        # Without this coroutine, none of the commands will be triggered.
        await self.bot.process_commands(interaction.message)

    @app_commands.command(
        name=string['command']['disconnect_vocal']['slash_command'],
        description=string['command']['disconnect_vocal']['description']
    )
    @app_commands.allowed_contexts(guilds=True)
    async def disconnect(self, interaction: discord.Interaction):
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
        voice_client = interaction.guild.voice_client

        # --- Bot is not connected ---
        if not voice_client or not voice_client.is_connected():
            await interaction.response.send_message(
                string['vocal']['bot_is_not_connected'],
                ephemeral=True
            )
            return

        # --- Else disconnect the bot ---
        await voice_client.disconnect(force=True)
        await interaction.response.send_message(
            string['vocal']['bot_disconnected_with_success'],
            ephemeral=True
        )

        # This function processes the commands that have been registered to the bot.
        # Without this coroutine, none of the commands will be triggered.
        await self.bot.process_commands(interaction.message)


async def setup(bot):
    """
    Adds this cog to the given bot.

    Args:
        bot (commands.Bot): The bot instance to which the cog will be added.
    """
    await bot.add_cog(VocalCommands(bot))
