"""
main.py

Entry point for the Discord bot.

Main responsibilities:
- Load the bot token from a .env file
- Initialize the bot with the required intents
- Define events (on_ready, on_member_join)
- Load cogs containing app_commands (slash commands)
- Start the bot

Structure:
- EVENTS: handle Discord events
- LOAD_APP_COMMANDS: load cogs
- MAIN: launch the bot
"""


import asyncio
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv


# Get bot token from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Enable intents for member events
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

# Create bot instance
bot = commands.Bot(command_prefix="/", intents=intents)


#######################################
#          LOAD APP_COMMANDS          #
#######################################

async def load_cogs():
    """
    Load all cogs for the bot.

    Each cog contains a set of app_commands (slash commands).
    Currently, only the 'fun' cog is loaded.
    """
    import cogs.events
    import cogs.fun
    import cogs.reddit

    await cogs.events.setup(bot)
    await cogs.fun.setup(bot)
    await cogs.reddit.setup(bot)


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
    await bot.start(TOKEN)


# Run the bot
asyncio.run(main())