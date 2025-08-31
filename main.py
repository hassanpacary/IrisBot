"""
main.py
© by hassanpacary

Entry point of the bot.
"""

# --- Imports ---
import asyncio
import datetime
import logging
import os
import sys

# --- Third party imports
import discord
from discord.ext import commands
from dotenv import load_dotenv

# --- Bot modules ---
import cogs.events_listener
import cogs.fun_commands
import cogs.reddit_commands
import cogs.vocal_commands

# Load environment variables from dotenv file
try:
    load_dotenv()
except OSError as e:
    logging.error(
        "%s -- Error: Unable to load environment variables.\n%s",
        datetime.datetime.now().strftime('%d.%m.%Y %T'), e
    )
    sys.exit()

# Setup logging file
logging.basicConfig(filename='log.txt', level=logging.INFO)

# Enable intents flags
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
intents.voice_states = True

# Create bot instance
bot_client = commands.Bot(command_prefix="/", intents=intents)


##########################
#          MAIN          #
##########################

async def main():
    """
    Main coroutine to start the bot.

    Steps:
    1. Load cogs
    2. Start the bot using the token
    """
    await cogs.events_listener.setup(bot_client)
    await cogs.fun_commands.setup(bot_client)
    await cogs.reddit_commands.setup(bot_client)
    await cogs.vocal_commands.setup(bot_client)

    await bot_client.start(os.getenv('DISCORD_TOKEN'))


# Run the bot
asyncio.run(main())
