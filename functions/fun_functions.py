"""
fun_functions.py
© by hassanpacary

Useful functions for replying to Discord messages with a predefined "feur" response.
"""

# --- Imports ---
import discord

# --- bot modules ---
from functions.functions import load_json

# Load config data from json files
config = load_json("config.json")
string = load_json(f"string_config_{config['config']['langage']}.json")


async def reply_feur(message: discord.Message):
    """
    Replies to a message with a predefined fun response.

    Event:
        Triggered when the bot calls this function in response to a message.

    Action:
        - Sends a reply to the given message containing the FUN_FEUR string.
    """
    await message.reply(string['fun']['reply_feur'])
