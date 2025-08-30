"""
json_loader.py
© by hassanpacary

Provides a helper function to load JSON files from the 'config/' directory safely.
"""

# --- Imports ---
import datetime
import json
import logging
import os


def load_json(file: str) -> dict:
    """
    Loads a JSON file from the 'config/' directory.

    Args:
        file (str): The filename of the JSON file.

    Returns:
        dict: Parsed JSON content.

    Exits the program if the file is missing or cannot be loaded.
    """
    json_file_path = os.path.join('config', file)

    # -- Json file not found ---
    if not os.path.exists(json_file_path):
        logging.error(str(datetime.datetime.now().strftime('%d.%m.%Y %T')) + ' -- Error: ' + f"File not found: {file}")
        return {}

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(
            str(datetime.datetime.now().strftime('%d.%m.%Y %T')) + ' -- Error: ' + f"Failed to load {file}: {e}")
        return {}
