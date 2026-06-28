"""Cogs package.

Contains feature domain package.
Each package exposes a setup() coroutine that registers its cogs
into the bot's commands tree.

© by hassanpacary
"""

# --- Internal ---
from bot.cogs import core, fun, guild, level, reddit, social


async def setup(bot) -> None:
    """Registers all active feature cogs into the bot.

    Iterates through each feature domain and calls its setup() coroutine.
    An entier cog can be skipped if its ACTIVE flag is set to FALSE,
    in config file.

    Args:
        bot: The Discord bot instance to register cogs into.
    """
    await core.setup(bot)
    await fun.setup(bot)
    await guild.setup(bot)
    await level.setup(bot)
    await reddit.setup(bot)
    await social.setup(bot)
