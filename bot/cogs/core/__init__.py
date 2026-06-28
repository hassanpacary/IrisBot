"""Core cog package.

Registers the CoreListeners cog, which handles bot lifecycle events.

© by hassanpacary
"""

# --- Standard library ---
import logging

# --- Internal ---
from bot.cogs.core import core_config, core_listeners


async def setup(bot) -> None:
    """Loads core cogs into the bot if its ACTIVE flag is TRUE
    in core_config.py.

    Args:
        bot: The Discord bot instance.
    """
    if core_config.ACTIVE:
        await bot.add_cog(core_listeners.CoreListeners(bot))
        logging.info("Core cog loaded successfully")
