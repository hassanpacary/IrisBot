"""
vocal_functions.py
© by hassanpacary

Useful functions for Text-to-Speech (TTS) module for Discord bot using Azure Cognitive Services.
"""

# --- Imports ---
import os
import re

# --- Third party imports ---
import azure.cognitiveservices.speech as speechsdk
import discord
from discord import FFmpegPCMAudio

# --- bot modules ---
from functions.functions import load_json

# Load config data from json files
config = load_json("config.json")


async def text_to_speech(self, message: discord.Message):
    """
    Converts a message's text to speech and plays it in the user's voice channel.

    Event:
        Triggered when the bot processes a message for text-to-speech playback.

    Action:
        - Cleans the message content by removing special characters.
        - Checks if the bot is connected to a voice channel; returns if not.
        - Ensures the output directory exists and sets up a filename for the .wav file.
        - Configures Azure Speech SDK with subscription, region, endpoint, and voice.
        - Generates a speech file (.wav) from the cleaned text.
        - Plays the generated speech in the connected voice channel if not already playing.
    """

    # Safe text without specials characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', message.content)

    voice_client = discord.utils.get(self.bot.voice_clients, guild=message.guild)

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, "tts_output.wav")

    # Defines configurations for speech
    speech_config = speechsdk.speech.SpeechConfig(subscription=os.getenv('AZURE_KEY'),
                                                  endpoint=os.getenv('AZURE_ENDPOINT'))
    speech_config.speech_synthesis_voice_name = config['config']['tts_speech_voice']

    # Save speech in .wav file
    audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)

    # Synthesizer the speech and wait result
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config
    )
    speech_synthesizer.speak_text_async(text).get()

    ffmpeg_path = os.path.join('tools', 'ffmpeg-8.0-essentials_build', 'bin', 'ffmpeg.exe')
    if not voice_client.is_playing():
        voice_client.play(FFmpegPCMAudio(executable=ffmpeg_path, source=filename))
