"""
bot/services/azure_service.py
© by hassanpacary

Useful services for Text-to-Speech (TTS) module for Discord bot using Azure Cognitive Services.
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

# --- FFMPEG EXE ---
FFMPEG_EXEC = os.path.join('tools', 'ffmpeg-8.0-essentials_build', 'bin', 'ffmpeg.exe')


#  █████╗ ███████╗██╗   ██╗██████╗ ███████╗    ███████╗███████╗██████╗ ██╗   ██╗██╗ ██████╗███████╗
# ██╔══██╗╚══███╔╝██║   ██║██╔══██╗██╔════╝    ██╔════╝██╔════╝██╔══██╗██║   ██║██║██╔════╝██╔════╝
# ███████║  ███╔╝ ██║   ██║██████╔╝█████╗      ███████╗█████╗  ██████╔╝██║   ██║██║██║     █████╗
# ██╔══██║ ███╔╝  ██║   ██║██╔══██╗██╔══╝      ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██║██║     ██╔══╝
# ██║  ██║███████╗╚██████╔╝██║  ██║███████╗    ███████║███████╗██║  ██║ ╚████╔╝ ██║╚██████╗███████╗
# ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝    ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚═╝ ╚═════╝╚══════╝


async def generate_speech_bytes(text: str) -> bytes:
    """
    Generate speech audio bytes from text using Azure Text-to-Speech.

    This function:
        - Uses Azure Speech SDK with subscription and endpoint from environment variables.
        - Sets the TTS voice from the bot configuration.
        - Writes the generated speech to a temporary WAV file.
        - Reads the WAV file into bytes and returns it.

    Args:
        text (str): The text to convert to speech.

    Returns:
        bytes: The speech audio in WAV format. Returns empty bytes if credentials are missing.
    """
    if not os.getenv('AZURE_KEY') or not os.getenv('AZURE_ENDPOINT'):
        logging.warning("Azure credentials not set")
        return b""

    speech_config = speechsdk.SpeechConfig(
        subscription=os.getenv('AZURE_KEY'),
        endpoint=os.getenv('AZURE_ENDPOINT')
    )
    speech_config.speech_synthesis_voice_name = BOT['voice']['synthesis_voice']

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        audio_config = speechsdk.audio.AudioOutputConfig(filename=tmp_file.name)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config, audio_config)
        synthesizer.speak_text_async(text).get()
        tmp_file.seek(0)
        return tmp_file.read()


async def play_audio_bytes(voice_client: discord.VoiceClient, audio_bytes: bytes):
    """
    Play audio from raw bytes in a Discord voice channel using a temporary file.

    This function:
        - Creates a temporary WAV file and writes the provided audio bytes to it.
        - Flushes the file to ensure the content is written to disk.
        - Plays the audio in the given Discord voice client if it is not already playing.
        - The temporary file is automatically deleted when closed.

    Args:
        voice_client (discord.VoiceClient): The voice client connected to the target voice channel.
        audio_bytes (bytes): Raw audio data in WAV format.
    """
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp_file:
        tmp_file.write(audio_bytes)
        tmp_file.flush()

        if not voice_client.is_playing():
            voice_client.play(FFmpegPCMAudio(executable=FFMPEG_EXEC, source=tmp_file.name))


async def text_to_speech(voice_client: discord.VoiceClient, message: discord.Message):
    """
    Converts a Discord message's text into speech and plays it in the specified voice channel.

    This function performs the following steps:
        - Cleans the message content by removing special characters.
        - Generates speech audio bytes from the cleaned text using a TTS service (e.g., Azure).
        - Plays the generated audio in the given Discord voice client.

    Args:
        voice_client (discord.VoiceClient): The voice client connected to the user's voice channel.
        message (discord.Message): The Discord message containing the text to convert.
    """
    text = sanitize_text(message.content)
    if not text:
        return

    audio_bytes = await generate_speech_bytes(text)
    await play_audio_bytes(voice_client, audio_bytes)
