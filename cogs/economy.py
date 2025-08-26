"""
economy.py

Cog containing economy slash commands for the bot.

Commands:
-
"""


from discord.ext import commands


class Economy(commands.Cog):
    """
    Cog containing economy commands for the bot.

    Attributes:
        bot (commands.Bot): The main bot instance.
    """

    def __init__(self, bot):
        """
        Initialize the cog with a reference to the bot.

        Args:
            bot (commands.Bot): The bot instance.
        """
        self.bot = bot


    # TODO - Economy and shop


async def setup(bot):
    """
    Adds this cog to the given bot.

    Args:
        bot (commands.Bot): The bot instance to which the cog will be added.
    """
    await bot.add_cog(Economy(bot))