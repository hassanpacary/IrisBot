"""Loads and exposes environment variables from the .env file.

Called at bot startup and exits immediately with a logged error if the
.env file is missing.

© by hassanpacary
"""

# --- Standard library ---
import logging
import os
import sys

# --- Third-party ---
from dotenv import find_dotenv, load_dotenv


def load_env() -> None:
    """Locates and loads the .env file.

    Raises:
        ValueError: If .env file not found,
        so that the bot never starts in a misconfigured state.
    """
    dotenv_path = find_dotenv()

    if not dotenv_path:
        raise ValueError("No .env file found, bot cannot start.")

    load_dotenv(dotenv_path)
    logging.info("Environment variables loaded from %s", dotenv_path)


def get_env_var(var: str) -> str:
    """Retrieves a required environment variable by name.

    Exits the process with code 1 if the "DISCORD_TOKEN" variable is absent or empty.

    Args:
        var: The name of the environment variable to retrieve.

    Returns:
        The value of the environment variable as a string, or a null string.
    """
    value = os.getenv(var)

    if not value:
        logging.error(
            "Required environment variable '%s' is not set.",
            var,
        )
        return "" if var != "DISCORD_TOKEN" else sys.exit(1)

    return value
