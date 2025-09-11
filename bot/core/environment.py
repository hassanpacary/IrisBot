"""
bot/core/environment.py
© by hassanpacary

configuration and load the environment variables.
"""

# --- Imports ---
import logging
import os
import sys
from dotenv import load_dotenv, find_dotenv


# ███████╗███╗   ██╗██╗   ██╗██╗██████╗  ██████╗ ███╗   ██╗███╗   ███╗███████╗███╗   ██╗████████╗
# ██╔════╝████╗  ██║██║   ██║██║██╔══██╗██╔═══██╗████╗  ██║████╗ ████║██╔════╝████╗  ██║╚══██╔══╝
# █████╗  ██╔██╗ ██║██║   ██║██║██████╔╝██║   ██║██╔██╗ ██║██╔████╔██║█████╗  ██╔██╗ ██║   ██║
# ██╔══╝  ██║╚██╗██║╚██╗ ██╔╝██║██╔══██╗██║   ██║██║╚██╗██║██║╚██╔╝██║██╔══╝  ██║╚██╗██║   ██║
# ███████╗██║ ╚████║ ╚████╔╝ ██║██║  ██║╚██████╔╝██║ ╚████║██║ ╚═╝ ██║███████╗██║ ╚████║   ██║
# ╚══════╝╚═╝  ╚═══╝  ╚═══╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝


def load_env() -> None:
    """
    Load environment variables from the .env file.

    Notes:
        - Exits the program if no `.env` file is found.
        - Must be called once at the start of the program.
    """
    dotenv_path = find_dotenv()

    # --- dotenv file not found ---
    if not dotenv_path:
        logging.error("No .env file found")
        sys.exit(1)

    load_dotenv(dotenv_path)
    logging.info("-- Environment variables loaded")


def get_env_var(key: str, required: bool = True) -> str | None:
    """
    Retrieve an environment variable safely.

    Args:
        key (str): The name of the environment variable.
        required (bool): If True, exit the program if the variable is missing.
                         If False, return None when not found.

    Returns:
        str | None: The value of the environment variable.

    Notes:
        - Use this instead of os.getenv directly for consistency.
    """
    env_variable = os.getenv(key)

    # --- Environment variable not found ---
    if not env_variable and required:
        logging.error(f"Required environment variable '{key}' not found.")
        sys.exit(1)

    return env_variable
