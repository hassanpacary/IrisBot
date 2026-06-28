"""Reddit cog package.

Registers the RedditCommands and RedditListeners cogs, which handles Reddit commands
and events.

© by hassanpacary
"""

# --- Standard library ---
import logging

# --- Internal ---
from bot.cogs.reddit import reddit_commands, reddit_config, reddit_listeners


async def setup(bot) -> None:
    """Loads reddit cogs into the bot if its ACTIVE flag is TRUE
    in reddit_config.py.

    Args:
        bot: The Discord bot instance.
    """
    if reddit_config.ACTIVE:
        await bot.add_cog(reddit_commands.RedditCommands(bot))
        await bot.add_cog(reddit_listeners.RedditListeners(bot))
        logging.info("Reddit cog loaded successfully")
