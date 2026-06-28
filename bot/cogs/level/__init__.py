"""Level cog package.

Registers the LevelAdminCommands, LevelCommands and LevelListeners cogs,
which handles experience/level commands and events.

© by hassanpacary
"""

# --- Standard library ---
import logging

# --- Internal ---
from bot.cogs.level import (
    level_admin_commands,
    level_commands,
    level_config,
    level_listeners,
)


async def setup(bot) -> None:
    """Loads level cogs into the bot if its ACTIVE flag is TRUE
    in level_config.py.

    Args:
        bot: The Discord bot instance.
    """
    if level_config.ACTIVE:
        await bot.add_cog(level_admin_commands.LevelAdminCommands(bot))
        await bot.add_cog(level_commands.LevelCommands(bot))
        await bot.add_cog(level_listeners.LevelListeners(bot))
        logging.info("Level cog loaded successfully")
