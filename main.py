"""
main.py
© by hassanpacary

Entry point of Irisbot.
"""

# --- Imports ---
import asyncio
import datetime

import discord
import logging
import os
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from dotenv file
try:
    load_dotenv()
except Exception as e:
    logging.error(datetime.datetime.now().strftime(
        '%d.%m.%Y %T') + ' -- Error: ' + f"Unable to load environment variables.\n" + str(e))
    exit()

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


#######################################
#          LOAD APP_COMMANDS          #
#######################################

async def load_cogs():
    """
    Load all cogs for the bot.

    Each cog contains a set of app_commands (slash commands).
    """
    import cogs.events_listener
    import cogs.fun_commands
    import cogs.reddit_commands
    import cogs.vocal_commands

    await cogs.events_listener.setup(bot_client)
    await cogs.fun_commands.setup(bot_client)
    await cogs.reddit_commands.setup(bot_client)
    await cogs.vocal_commands.setup(bot_client)


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
    await load_cogs()
    await bot_client.start(os.getenv('DISCORD_TOKEN'))


# Run the bot
asyncio.run(main())
