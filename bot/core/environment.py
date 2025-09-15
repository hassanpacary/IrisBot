"""
bot/core/environment.py
© by hassanpacary

configuration and load the environment variables
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
    """Load environment variables from the .env file"""
    dotenv_path = find_dotenv()

    # --- dotenv file not found ---
    if not dotenv_path:
        logging.error("No .env file found")
        sys.exit(1)

    load_dotenv(dotenv_path)
    logging.info("-- Environment variables loaded")


def get_env_var(var: str) -> str:
    """
    Retrieve an environment variable safely

    Parameters:
        var (str): The name of the environment variable to retrieve

    Returns:
        str: The value of the environment variable
    """
    env_variable = os.getenv(var)

    # --- Environment variable not found ---
    if not env_variable:
        logging.error(f"Required environment variable '{var}' not found.")
        sys.exit(1)

    return env_variable
