"""Social cog package.

Registers the SocialCommands cog, which handles social commands and events.

© by hassanpacary
"""

# --- Standard library ---
import logging

# --- Internal ---
from bot.cogs.social import social_commands, social_config


async def setup(bot) -> None:
    """Loads social cogs into the bot if its ACTIVE flag is TRUE
    in social_config.py.

    Args:
        bot: The Discord bot instance.
    """
    if social_config.ACTIVE:
        await bot.add_cog(social_commands.SocialCommands(bot))
        logging.info("Social cog loaded successfully")
