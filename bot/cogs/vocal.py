"""
bot/cogs/vocal.py
© by hassanpacary

Cog containing vocal slash commands and their logic
"""

# --- Imports ---
import logging

# --- Third party imports ---
import discord
from discord import app_commands
from discord.ext import commands

# --- Bot modules ---
from bot.core.config_loader import BOT, COMMANDS
from bot.services.vocal.azure_service import text_to_speech
from bot.services.vocal.vocal_service import join_channel, disconnect_channel


#  ██████╗██╗  ██╗ █████╗ ████████╗██████╗  ██████╗ ████████╗
# ██╔════╝██║  ██║██╔══██╗╚══██╔══╝██╔══██╗██╔═══██╗╚══██╔══╝
# ██║     ███████║███████║   ██║   ██████╔╝██║   ██║   ██║
# ██║     ██╔══██║██╔══██║   ██║   ██╔══██╗██║   ██║   ██║
# ╚██████╗██║  ██║██║  ██║   ██║   ██████╔╝╚██████╔╝   ██║
#  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═════╝  ╚═════╝    ╚═╝


class VocalCog(commands.Cog):
    """Vocal cog class"""

    def __init__(self, bot):
        """Initialize the cog with a reference to the bot"""
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
        Event listener that triggers whenever a message is sent in a channel

        Parameters:
            message (discord.Message): The message who trigger the listener

        Actions:
            - Check if the message is sent in the vocal channel (textuel) and if the bot is in vocal
            - If matched, calls text_to_speech

        this event converts what users send in a text channel,
         into audio played by the bot connected in a voice channel
        """
        channel_id = BOT['channels']['tts']

        # --- Ignore bot message ---
        if message.author == self.bot.user:
            return

        bot_voice = discord.utils.get(self.bot.voice_clients, guild=message.guild)
        if bot_voice and message.channel.id == channel_id:
            author_voice = message.author.voice

            if author_voice and author_voice.channel == bot_voice.channel:
                logging.info(
                    "-- %s send %s and was played by the bot in vocal channel",
                    message.author.name,
                    message.content
                )
                await text_to_speech(ctx=bot_voice, message=message)

        await self.bot.process_commands(message)

    # pylint: disable=line-too-long
    #  ██████╗ ██████╗ ███╗   ███╗███╗   ███╗ █████╗ ███╗   ██╗██████╗ ███████╗    ██╗      ██████╗  ██████╗ ██╗ ██████╗
    # ██╔════╝██╔═══██╗████╗ ████║████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝    ██║     ██╔═══██╗██╔════╝ ██║██╔════╝
    # ██║     ██║   ██║██╔████╔██║██╔████╔██║███████║██╔██╗ ██║██║  ██║███████╗    ██║     ██║   ██║██║  ███╗██║██║
    # ██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║  ██║╚════██║    ██║     ██║   ██║██║   ██║██║██║
    # ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║██████╔╝███████║    ███████╗╚██████╔╝╚██████╔╝██║╚██████╗
    #  ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝    ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝ ╚═════╝
    # pylint: enable=line-too-long

    @app_commands.command(
        name=COMMANDS['vocal']['join']['slash_command'],
        description=COMMANDS['vocal']['join']['description'],
    )
    async def join_logic(self, interaction: discord.Interaction):
        """
        Responds to the /join slash command

        Parameters:
            interaction (discord.Interaction): The interaction object triggered by the user

        Action:
            - If the user is not in a voice channel, sends an ephemeral message
            - If the bot is already connected to the same channel, sends an ephemeral message
            - If the bot is connected to a different voice channel, moves the bot
            - If the bot is not connected, joins the user's voice channel
        """
        logging.info(
            "-- %s use /join slash command",
            interaction.user.name
        )
        bot_voice = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        await join_channel(ctx=interaction, bot_voice=bot_voice)

    @app_commands.command(
        name=COMMANDS['vocal']['disconnect']['slash_command'],
        description=COMMANDS['vocal']['disconnect']['description'],
    )
    async def disconnect_logic(self, interaction: discord.Interaction):
        """
        Responds to the /join slash command

        Parameters:
            interaction (discord.Interaction): The interaction object triggered by the user

        Action:
            - If the bot is not connected, sends an ephemeral message
            - If the bot is connected, disconnects from the voice channel
        """
        logging.info(
            "-- %s use /disconnect slash command",
            interaction.user.name
        )
        await disconnect_channel(ctx=interaction)


async def setup(bot):
    """Adds this cog to the given bot"""
    await bot.add_cog(VocalCog(bot))
