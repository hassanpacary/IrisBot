"""Discord bot class extending commands.Bot.

© by hassanpacary
"""

# --- Third-party ---
from discord.ext import commands

# --- Internal ---
from bot import cogs
from bot.features import context_menus, tasks
from bot.services.core import core_service
from bot.utils import db_manager


class Bot(commands.Bot):
    """Discord bot with dynamic intents configuration and database initiation.

    Attributes:
        colors_db: Database manager for colors datas.
        levels_db: Database manager for levels datas.
    """

    def __init__(self) -> None:
        self.colors_db = db_manager.DatabaseManager("colors.db")
        self.levels_db = db_manager.DatabaseManager("levels.db")

        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=core_service.build_intents(),
        )

    async def setup_hook(self) -> None:
        """Initializes databases, cogs, tasks and context menus
        before connecting to Discord.

        Called automatically by discord.py as part of the bot lifecycle,
        before the WebSocket connection is established.
        """
        await core_service.init_databases(bot=self)

        await context_menus.setup(bot=self)
        await tasks.start(bot=self)

        await cogs.setup(bot=self)
        await self.tree.sync()
