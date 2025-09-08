"""
bot/utils/files_utils.py
© by hassanpacary

Utils functions for files manipulations.
"""

# --- Imports ---
import os
import logging
import json

# --- Third party imports ---
import yaml


# ██╗      ██████╗  █████╗ ██████╗     ███████╗██╗██╗     ███████╗
# ██║     ██╔═══██╗██╔══██╗██╔══██╗    ██╔════╝██║██║     ██╔════╝
# ██║     ██║   ██║███████║██║  ██║    █████╗  ██║██║     █████╗
# ██║     ██║   ██║██╔══██║██║  ██║    ██╔══╝  ██║██║     ██╔══╝
# ███████╗╚██████╔╝██║  ██║██████╔╝    ██║     ██║███████╗███████╗
# ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝     ╚═╝     ╚═╝╚══════╝╚══════╝


def load_file(file_path: str, mode: str) -> str | bytes:
    """
    Load a text file safely and return its content.

    Args:
        file_path (str): Path to the file.
        mode (str): File mode.

    Returns:
        str: File content, or empty string if error occurs.
    """
    if not os.path.exists(file_path):
        logging.error("File not found: %s", file_path)
        return ""

    # --- Read the file and return it ---
    try:
        with open(file_path, mode, encoding='utf-8' if mode == "r" else None) as f:
            return f.read()

    except OSError as e:
        logging.error("Error reading %s.\n%s", file_path, e)
        return ""


# ██╗    ██╗██████╗ ██╗████████╗███████╗
# ██║    ██║██╔══██╗██║╚══██╔══╝██╔════╝
# ██║ █╗ ██║██████╔╝██║   ██║   █████╗
# ██║███╗██║██╔══██╗██║   ██║   ██╔══╝
# ╚███╔███╔╝██║  ██║██║   ██║   ███████╗
#  ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝


def write_file(file_path: str, data: bytes) -> bool:
    """
    Safely write raw bytes to a file.

    Args:
        file_path (str): Path to the file where data should be written.
        data (bytes): The binary content to write.

    Returns:
        bool: True if the file was written successfully, False otherwise.
    """
    # --- Try writing the file ---
    try:
        with open(file_path, "wb") as f:
            f.write(data)
        return True

    except OSError as e:
        logging.error("Error writing %s.\n%s", file_path, e)
        return False


#      ██╗███████╗ ██████╗ ███╗   ██╗    ███████╗██╗██╗     ███████╗
#      ██║██╔════╝██╔═══██╗████╗  ██║    ██╔════╝██║██║     ██╔════╝
#      ██║███████╗██║   ██║██╔██╗ ██║    █████╗  ██║██║     █████╗
# ██   ██║╚════██║██║   ██║██║╚██╗██║    ██╔══╝  ██║██║     ██╔══╝
# ╚█████╔╝███████║╚██████╔╝██║ ╚████║    ██║     ██║███████╗███████╗
#  ╚════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝    ╚═╝     ╚═╝╚══════╝╚══════╝


def load_json(file_path: str) -> dict:
    """Load a JSON file using the generic load_file function."""
    content = load_file(file_path, "r")

    # --- The file is empty ---
    if not content:
        return {}

    # --- Return json content of the file ---
    try:
        return json.loads(content)

    except json.JSONDecodeError as e:
        logging.error("Failed to decode JSON.\n%s", e)
        return {}


# ██╗   ██╗ █████╗ ███╗   ███╗██╗         ███████╗██╗██╗     ███████╗
# ╚██╗ ██╔╝██╔══██╗████╗ ████║██║         ██╔════╝██║██║     ██╔════╝
#  ╚████╔╝ ███████║██╔████╔██║██║         █████╗  ██║██║     █████╗
#   ╚██╔╝  ██╔══██║██║╚██╔╝██║██║         ██╔══╝  ██║██║     ██╔══╝
#    ██║   ██║  ██║██║ ╚═╝ ██║███████╗    ██║     ██║███████╗███████╗
#    ╚═╝   ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝    ╚═╝     ╚═╝╚══════╝╚══════╝


def load_yaml(file_path: str) -> dict:
    """Load a YAML file using the generic load_file function."""
    content = load_file(file_path, "r")

    # --- The file is empty ---
    if not content:
        return {}

    # --- Return yaml content of the file ---
    try:
        return yaml.safe_load(content)

    except yaml.YAMLError as e:
        logging.error("Failed to decode YAML.\n%s", e)
        return {}


# ██╗      ██████╗  █████╗ ██████╗      ██████╗ ██████╗ ███╗   ██╗███████╗██╗ ██████╗
# ██║     ██╔═══██╗██╔══██╗██╔══██╗    ██╔════╝██╔═══██╗████╗  ██║██╔════╝██║██╔════╝
# ██║     ██║   ██║███████║██║  ██║    ██║     ██║   ██║██╔██╗ ██║█████╗  ██║██║  ███╗
# ██║     ██║   ██║██╔══██║██║  ██║    ██║     ██║   ██║██║╚██╗██║██╔══╝  ██║██║   ██║
# ███████╗╚██████╔╝██║  ██║██████╔╝    ╚██████╗╚██████╔╝██║ ╚████║██║     ██║╚██████╔╝
# ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝      ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝ ╚═════╝


def load_all_configs() -> dict:
    """
    Load all required JSON config files into a single dictionary.

    Returns:
        dict: A dictionary with loaded configs.
    """
    base_path = os.path.join("bot", "config")
    config = {}

    # Load all configuration json in a config dict
    for filename in os.listdir(base_path):
        file_path = os.path.join(base_path, filename)

        if not os.path.isfile(file_path) or not filename.endswith(".json"):
            continue

        # Skip language strings, they will be loaded later
        if filename.startswith("strings."):
            continue

        name, ext = os.path.splitext(filename)
        config[name] = load_json(file_path)

    # corrects language data according to language
    lang = config["bot"]["langage"]
    config["strings"] = load_json(os.path.join(base_path, f"strings.{lang}.json"))

    return config
