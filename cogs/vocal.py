"""
vocal.py

Cog containing vocal slash commands for the bot.

Commands:
- join: Join vocal channel
- disconnect: Disconnect vocal channel
"""


import discord
from discord import app_commands
from discord.ext import commands
from config.string_fr import (VOCAL_USER_NOT_CONNECTED, VOCAL_IRIS_CONNECT_SUCCESS, VOCAL_IRIS_NOT_CONNECTED,
                              VOCAL_IRIS_DISCONNECT_SUCCESS, VOCAL_IRIS_ALREADY_CONNECTED, VOCAL_IRIS_CHANGE_CHANNEL)


class Vocal(commands.Cog):
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


    @app_commands.command(name="join", description="Iris rejoint le salon vocal.")
    @app_commands.guild_only()
    async def join(self, interaction: discord.Interaction):
        """
        Command for the bot Iris to join a voice channel.

        Functionality:
        - Checks if the user invoking the command is connected to a voice channel.
        - If the user is not in a voice channel, sends an ephemeral warning message.
        - Checks if the bot is already connected to a voice channel.
        - If the bot is already in the same channel as the user, sends an ephemeral message indicating it is already connected.
        - If the bot is connected to a different channel, moves the bot to the user's channel and sends an ephemeral confirmation message.
        - If the bot is not connected to any voice channel, it joins the user's channel and sends an ephemeral confirmation message.

        Parameters:
        - interaction (discord.Interaction): The Interaction object representing the slash command invoked by the user.

        Behavior:
        - Safely handles cases where the user is not in a voice channel or the bot is not connected.
        - All confirmation messages are sent ephemerally to avoid spamming the channel.
        """
        user = interaction.user
        bot_voice_client = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)

        # User is connected in vocal channel
        if not user.voice or not user.voice.channel:
            await interaction.response.send_message(VOCAL_USER_NOT_CONNECTED, ephemeral=True)
            return

        # Bot is already connected in vocal channel
        elif bot_voice_client is not None and bot_voice_client.channel == user.voice.channel:
            await interaction.response.send_message(VOCAL_IRIS_ALREADY_CONNECTED, ephemeral=True)
            return

        # Bot is not in the same vocal channel of the user
        elif bot_voice_client is not None and bot_voice_client.channel != user.voice.channel:
            await bot_voice_client.move_to(user.voice.channel)
            await interaction.response.send_message(VOCAL_IRIS_CHANGE_CHANNEL, ephemeral=True)

        await user.voice.channel.connect()
        await interaction.response.send_message(VOCAL_IRIS_CONNECT_SUCCESS, ephemeral=True)


    @app_commands.command(name="disconnect", description="Déconnecte Iris du salon vocal.")
    @app_commands.allowed_contexts(guilds=True)
    async def disconnect(self, interaction: discord.Interaction):
        """
        Disconnect command for Discord bot.

        This command disconnects the bot (Iris) from the voice channel in the server.

        Function:
        - disconnect(interaction: discord.Interaction):
            Disconnects the bot from the current voice channel if connected.
            Sends a confirmation message if successful, or an ephemeral warning if the bot is not connected.
        """
        voice_client = interaction.guild.voice_client

        if not voice_client or not voice_client.is_connected():
            await interaction.response.send_message(VOCAL_IRIS_NOT_CONNECTED, ephemeral=True)
            return

        await voice_client.disconnect(force=True)
        await interaction.response.send_message(VOCAL_IRIS_DISCONNECT_SUCCESS, ephemeral=True)


async def setup(bot):
    """
    Adds this cog to the given bot.

    Args:
        bot (commands.Bot): The bot instance to which the cog will be added.
    """
    await bot.add_cog(Vocal(bot))