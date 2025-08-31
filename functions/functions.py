"""
json_loader.py
© by hassanpacary

Useful functions for to load files directory safely.
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
        logging.error(
            '%s -- Error: File not found: %s',
            datetime.datetime.now().strftime('%d.%m.%Y %T'), file
        )
        return {}

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(
            '%s -- Error: File not found: %s',
            datetime.datetime.now().strftime('%d.%m.%Y %T'), json_file_path
        )
    except json.JSONDecodeError as e:
        logging.error(
            '%s -- Error: Failed to decode JSON in %s.\n%s',
            datetime.datetime.now().strftime('%d.%m.%Y %T'), json_file_path, e
        )
    except OSError as e:
        logging.error(
            '%s -- Error: OS error while reading %s.\n%s',
            datetime.datetime.now().strftime('%d.%m.%Y %T'), json_file_path, e
        )

    return {}


async def load_graphql_query(query: str) -> str:
    """
    Loads a GraphQL query from the 'queries/' directory.

    Args:
        query (str): The filename of the .graphql query file.

    Returns:
        str: The GraphQL query string, or an empty string if loading fails.
    """
    graphql_query_file_path = os.path.join('queries', query)

    # -- Query file not found ---
    if not os.path.exists(graphql_query_file_path):
        logging.error(
            '%s -- Error: File not found: %s',
            datetime.datetime.now().strftime('%d.%m.%Y %T'), query
        )
        return ""

    try:
        with open(graphql_query_file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        logging.error(
            '%s -- Error: File not found: %s',
            datetime.datetime.now().strftime('%d.%m.%Y %T'), query
        )
    except OSError as e:
        logging.error(
            '%s -- Error: OS error while reading %s.\n%s',
            datetime.datetime.now().strftime('%d.%m.%Y %T'), query, e
        )

    return ""
