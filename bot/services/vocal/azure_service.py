"""
bot/services/azure_service.py
© by hassanpacary

Utility functions for Text-to-Speech (TTS) module for Discord bot using Azure Cognitive Services.
"""

# --- Imports ---
import os
import logging
import tempfile

# --- Third party imports ---
import azure.cognitiveservices.speech as speechsdk
import discord
from discord import FFmpegPCMAudio

# --- bot modules ---
from bot.core.config_loader import BOT
from bot.utils.strings_utils import sanitize_text


#  █████╗ ███████╗██╗   ██╗██████╗ ███████╗    ███████╗███████╗██████╗ ██╗   ██╗██╗ ██████╗███████╗
# ██╔══██╗╚══███╔╝██║   ██║██╔══██╗██╔════╝    ██╔════╝██╔════╝██╔══██╗██║   ██║██║██╔════╝██╔════╝
# ███████║  ███╔╝ ██║   ██║██████╔╝█████╗      ███████╗█████╗  ██████╔╝██║   ██║██║██║     █████╗
# ██╔══██║ ███╔╝  ██║   ██║██╔══██╗██╔══╝      ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██║██║     ██╔══╝
# ██║  ██║███████╗╚██████╔╝██║  ██║███████╗    ███████║███████╗██║  ██║ ╚████╔╝ ██║╚██████╗███████╗
# ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝    ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚═╝ ╚═════╝╚══════╝


async def _generate_speech_bytes(text: str) -> bytes:
    """
    Generate speech audio bytes from text using Azure Text-to-Speech

    Parameters:
        text (str): The text to convert to speech

    Actions:
        - Sets the TTS voice from the bot configuration
        - Writes the generated speech to a temporary WAV file
        - Reads the WAV file into bytes and returns it

    Returns:
        bytes: The speech audio in WAV format. Returns empty bytes if credentials are missing
    """
    azure_key = os.getenv('AZURE_KEY')
    azure_endpoint = os.getenv('AZURE_ENDPOINT')

    synthesis_voice = BOT['voice']['synthesis_voice']

    # --- Credentials are missing ---
    if not azure_key or not azure_endpoint:
        logging.warning("Azure credentials not set")
        return b""

    # Configure speech SDK
    speech_config = speechsdk.SpeechConfig(
        subscription=azure_key,
        endpoint=azure_endpoint
    )
    speech_config.speech_synthesis_voice_name = synthesis_voice

    # Write the generated speech to a WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        audio_config = speechsdk.audio.AudioOutputConfig(filename=tmp_file.name)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config, audio_config)

        synthesizer.speak_text_async(text).get()

        tmp_file.seek(0)
        return tmp_file.read()


async def _play_audio_bytes(ctx: discord.VoiceClient, audio_bytes: bytes):
    """
    Play audio from raw bytes in a Discord voice channel using a temporary file

    Parameters:
        ctx (discord.VoiceClient): The voice client connected to the user's voice channel
        audio_bytes (bytes): Raw audio data in WAV format

    Actions:
        - Plays the audio in the given Discord voice client if it is not already playing
    """
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp_file:
        tmp_file.write(audio_bytes)
        tmp_file.flush()

        if not ctx.is_playing():
            ctx.play(FFmpegPCMAudio(source=tmp_file.name))


async def text_to_speech(ctx: discord.VoiceClient, message: discord.Message):
    """
    Converts a Discord message's text into speech and plays it in the specified voice channel

    Parameters:
        ctx (discord.VoiceClient): The voice client connected to the user's voice channel
        message (discord.Message): The Discord message containing the text to convert

    Actions:
        - Cleans the message content by removing special characters
        - Generates speech audio bytes from the cleaned text using a TTS service
        - Plays the generated audio in the given Discord voice client
    """
    text = sanitize_text(text=message.content)

    audio_bytes = await _generate_speech_bytes(text=text)
    await _play_audio_bytes(ctx=ctx, audio_bytes=audio_bytes)
