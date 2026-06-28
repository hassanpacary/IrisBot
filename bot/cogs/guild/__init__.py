"""Guild cog package.

Registers the GuildAdminCommands and GuildListeners cogs, which guild admin-only
commands and events.

© by hassanpacary
"""

# --- Standard library ---
import logging

# --- Internal ---
from bot.cogs.guild import guild_admin_commands, guild_config, guild_listeners


async def setup(bot) -> None:
    """Loads guild cogs into the bot if its ACTIVE flag is TRUE
    in guild_config.py.

    Args:
        bot: The Discord bot instance.
    """
    if guild_config.ACTIVE:
        await bot.add_cog(guild_admin_commands.GuildAdminCommands(bot))
        await bot.add_cog(guild_listeners.GuildListeners(bot))
        logging.info("Guild cog loaded successfully")
