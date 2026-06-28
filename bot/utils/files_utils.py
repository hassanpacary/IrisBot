"""Files utilities functions.

Manage utilities functions for multiples files operations.
Like load and write safe functions for bytes files.
And load and write safe functions for JSON files.
All functions log errors and return safe defaults on failure rather

© by hassanpacary
"""

# --- Standard library ---
import json
import logging
from pathlib import Path


async def load_file(fp: str) -> bytes:
    """Reads a file and returns its Bytes content.

    Args:
        fp: Path to the file, relative to the project root.

    Returns:
        The file content as bytes or null bytes string on failure.
    """
    try:
        with open(file=fp, mode="rb") as f:
            return f.read()
    except OSError as e:
        logging.error("Error reading %s: %s", fp, e)
        return b""


async def load_json(fp: Path) -> dict:
    """Reads JSON file and returns its content.

    Args:
        fp: Path to the JSON file, relative to the project root.

    Returns:
        The parsed JSON content as a dict, or an empty dict on error.
    """
    try:
        return json.loads(fp.read_text(encoding="utf-8"))
    except FileNotFoundError:
        logging.error("Deals list file not found: %s", fp)
        return {}
    except json.JSONDecodeError as e:
        logging.error("Failed to parse deals list file: %s", e)
        return {}


async def write_file(fp: str, data: bytes) -> bool:
    """Writes raw bytes to a file.

    Args:
        fp: Absolute or relative path to the output file.
        data: The binary content to write.

    Returns:
        True if write succeeded, False otherwise.
    """
    try:
        with open(fp, "wb") as f:
            f.write(data)
        return True
    except OSError as e:
        logging.error("Error writing bytes to %s: %s", fp, e)
        return False


async def write_json(fp: Path, data: dict | list) -> None:
    """Writes data to a JSON file.

    Args:
        fp: Path to the JSON file, relative to the project root.
        data: The dict data to write. Must be JSON-serializable.

    Raises:
        OSError: If writing fails.
        TypeError: If data is not JSON serializable.
    """
    try:
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except OSError as e:
        logging.error("Error writing JSON to %s: %s", fp, e)
    except TypeError as e:
        logging.error("Data is not JSON serializable: %s", e)
