"""
bot/core/config_loader.py
© by hassanpacary

Load and store all configuration json.
"""

# --- Imports ---
import os

# --- Bot modules ---
from bot.utils.files_utils import load_json

#  ██████╗ ██████╗ ███╗   ██╗███████╗██╗ ██████╗     ██╗      ██████╗  █████╗ ██████╗ ███████╗██████╗
# ██╔════╝██╔═══██╗████╗  ██║██╔════╝██║██╔════╝     ██║     ██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
# ██║     ██║   ██║██╔██╗ ██║█████╗  ██║██║  ███╗    ██║     ██║   ██║███████║██║  ██║█████╗  ██████╔╝
# ██║     ██║   ██║██║╚██╗██║██╔══╝  ██║██║   ██║    ██║     ██║   ██║██╔══██║██║  ██║██╔══╝  ██╔══██╗
# ╚██████╗╚██████╔╝██║ ╚████║██║     ██║╚██████╔╝    ███████╗╚██████╔╝██║  ██║██████╔╝███████╗██║  ██║
#  ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝ ╚═════╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝


# General bot configuration data. Like langage, guild, intents, channels ...
BOT = load_json(os.path.join("bot", "config", "bot.json"))

# List of all bot commands. Contains their name and description
COMMANDS = load_json(os.path.join("bot", "config", "commands.json"))

# All bot response strings according to the language defined in bot.json
STRINGS = load_json(os.path.join("bot", "config", f"strings.{BOT['langage']}.json"))

# List of regexes used
REGEX = load_json(os.path.join("bot", "config", "regex.json"))
