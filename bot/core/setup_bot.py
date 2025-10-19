"""
bot/core/setup_bot.py
© by hassanpacary

Custom Discord bot class with automated configuration and cog loading
"""

# --- Third party imports ---
import discord
from discord.ext import commands

# --- Bot modules ---
from bot.core.config_loader import BOT
from bot.services.guild.cogs_factory import load_cogs
from bot.utils.db_manager import DatabaseManager


# ██████╗  ██████╗ ████████╗
# ██╔══██╗██╔═══██╗╚══██╔══╝
# ██████╔╝██║   ██║   ██║
# ██╔══██╗██║   ██║   ██║
# ██████╔╝╚██████╔╝   ██║
# ╚═════╝  ╚═════╝    ╚═╝


class Bot(commands.Bot):
    """Discord bot class"""

    def __init__(self) -> None:
        """Initialize the bot with a default command prefix and enabled intents"""
        bot = BOT

        # Initialize intents dynamically
        intents = discord.Intents.default()
        for intent_name, enabled in bot.get("intents", {}).items():
            if hasattr(intents, intent_name):
                setattr(intents, intent_name, enabled)

        self.level_db = DatabaseManager("level.db")

        # Initialize bot
        super().__init__(command_prefix="/", intents=intents)

    async def setup_hook(self) -> None:
        """Lifecycle hook called automatically before the bot connects to Discord"""
        await load_cogs(self)
        await self.tree.sync()
