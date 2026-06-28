"""Fun cog package.

Registers the FunCommands and FunListeners cogs, which handles funny commands
and events.

© by hassanpacary
"""

# --- Standard library ---
import logging

# --- Internal ---
from bot.cogs.fun import fun_commands, fun_config, fun_listeners


async def setup(bot) -> None:
    """Loads fun cogs into the bot if its ACTIVE flag is TRUE
    in fun_config.py.

    Args:
        bot: The Discord bot instance.
    """
    if fun_config.ACTIVE:
        await bot.add_cog(fun_commands.FunCommands(bot))
        await bot.add_cog(fun_listeners.FunListeners(bot))
        logging.info("Fun cog loaded successfully")
