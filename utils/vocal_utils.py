"""
Text-to-Speech (TTS) module for Discord bot using Azure Cognitive Services.

This module allows the Discord bot to:
- Generate speech audio files from user messages using Azure Cognitive Services Speech.
- Play the generated speech in a Discord voice channel using FFmpeg.
- Sanitize message text by removing special characters before sending it to the TTS engine.

Requirements:
- Azure Cognitive Services Speech SDK
- FFmpeg installed and accessible (path configured in config.constants.FFMPEG_PATH)
- Discord.py library

Environment variables required:
- AZURE_KEY: Azure subscription key
- AZURE_ENDPOINT: Azure endpoint URL
- AZURE_REGION: Azure service region
"""


import azure.cognitiveservices.speech as speechsdk
import discord
import os
import re
from discord import FFmpegPCMAudio
from config.constants import FFMPEG_PATH


AZURE_KEY = os.getenv("AZURE_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_REGION = os.getenv("AZURE_REGION")


async def text_to_speech(self, message: discord.Message):
    """
    Convert a Discord message into speech and play it in the bot's voice channel.

    Steps:
    1. Sanitize the message content by removing special characters.
    2. Generate speech audio from text using Azure Cognitive Services Speech.
    3. Save the speech to a temporary WAV file.
    4. Play the audio file in the Discord voice channel using FFmpeg.

    Parameters
    ----------
    self : commands.Cog or bot instance
        The calling object that contains the Discord bot instance (`self.bot`).
    message : discord.Message
        The Discord message object containing the text to be spoken.

    Notes
    -----
    - The function assumes the bot is already connected to a voice channel.
    - If the bot is not connected or is already playing audio, the function will return early.
    - The synthesized voice is set to "fr-FR-VivienneMultilingualNeural".
    """

    # Safe text without specials characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', message.content)

    voice_client = discord.utils.get(self.bot.voice_clients, guild=message.guild)
    if not voice_client.is_connected():
        return

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, "tts_output.wav")

    speech_config = speechsdk.speech.SpeechConfig(subscription=AZURE_KEY, region=AZURE_REGION, endpoint=AZURE_ENDPOINT)
    speech_config.speech_synthesis_voice_name = "fr-FR-VivienneMultilingualNeural"

    # Save speech in .wav file
    audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)

    # Performs synthesis on plain text
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesizer.speak_text_async(text).get()

    if not voice_client.is_playing():
        voice_client.play(FFmpegPCMAudio(executable=FFMPEG_PATH, source=filename))