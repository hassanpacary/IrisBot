"""
bot/utils/discord_utils.py
© by hassanpacary

Utility functions for discord.
"""

# --- Imports ---
import io
import logging

# --- Third party imports ---
import discord


# ██████╗ ███████╗███████╗██████╗  ██████╗ ███╗   ██╗███████╗███████╗     ██████╗ ██████╗ ███╗   ██╗███████╗████████╗██████╗ ██╗   ██╗ ██████╗████████╗ ██████╗ ██████╗
# ██╔══██╗██╔════╝██╔════╝██╔══██╗██╔═══██╗████╗  ██║██╔════╝██╔════╝    ██╔════╝██╔═══██╗████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║   ██║██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
# ██████╔╝█████╗  ███████╗██████╔╝██║   ██║██╔██╗ ██║███████╗█████╗      ██║     ██║   ██║██╔██╗ ██║███████╗   ██║   ██████╔╝██║   ██║██║        ██║   ██║   ██║██████╔╝
# ██╔══██╗██╔══╝  ╚════██║██╔═══╝ ██║   ██║██║╚██╗██║╚════██║██╔══╝      ██║     ██║   ██║██║╚██╗██║╚════██║   ██║   ██╔══██╗██║   ██║██║        ██║   ██║   ██║██╔══██╗
# ██║  ██║███████╗███████║██║     ╚██████╔╝██║ ╚████║███████║███████╗    ╚██████╗╚██████╔╝██║ ╚████║███████║   ██║   ██║  ██║╚██████╔╝╚██████╗   ██║   ╚██████╔╝██║  ██║
# ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚══════╝     ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝  ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝


async def send_response_to_discord(
        target: discord.Interaction | discord.Message,
        content: str = None,
        files: list[discord.File] = None,
        ephemeral: bool = False
) -> None:
    """
    Send a response to either a Discord Message or an Interaction.

    Args:
        target (discord.Message | Interaction): The message or interaction to respond to.
        content (str): The message text (optional).
        files (list[discord.File]): The files to send.
        ephemeral (bool): Whether the response should be ephemeral (only works with interactions).
    """
    if files is None:
        files = []

    # --- Response to Slash command ---
    if isinstance(target, discord.Interaction):
        if target.response.is_done():  # type: ignore
            await target.followup.send(content=content, files=files, ephemeral=ephemeral)
        else:
            await target.response.send_message(content=content, files=files, ephemeral=ephemeral)  # type: ignore

    # --- Response to user message ---
    elif isinstance(target, discord.Message):
        await target.reply(content=content, files=files)

    logging.info(f"-- Discord message has been sent: {content} with files: {files}")





#  ██████╗██████╗ ███████╗ █████╗ ████████╗███████╗    ███████╗██╗██╗     ███████╗
# ██╔════╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔════╝    ██╔════╝██║██║     ██╔════╝
# ██║     ██████╔╝█████╗  ███████║   ██║   █████╗      █████╗  ██║██║     █████╗
# ██║     ██╔══██╗██╔══╝  ██╔══██║   ██║   ██╔══╝      ██╔══╝  ██║██║     ██╔══╝
# ╚██████╗██║  ██║███████╗██║  ██║   ██║   ███████╗    ██║     ██║███████╗███████╗
#  ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝    ╚═╝     ╚═╝╚══════╝╚══════╝


def create_discord_file(data: bytes, filename: str) -> discord.File:
    """
    Create a discord.File object from raw bytes.

    Args:
        data (bytes): Raw file data.
        filename (str): Filename to assign to the file.

    Returns:
        discord.File: A Discord-compatible file object.
    """
    return discord.File(io.BytesIO(data), filename=filename)
