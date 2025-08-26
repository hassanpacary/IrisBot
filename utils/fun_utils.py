import discord
from config.string_fr import FUN_FEUR


async def reply_feur(message: discord.Message):
    """
    Reply to a Discord message with the predefined "feur" response.

    Args:
        message (discord.Message): The message to reply to.
    """
    await message.reply(FUN_FEUR)