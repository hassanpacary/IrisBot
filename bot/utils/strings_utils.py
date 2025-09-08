"""
bot/utils/strings_utils.py
© by hassanpacary

Utility functions for string manipulation, formatting, and parsing.
"""

# --- Imports ---
import re
from urllib.parse import urlparse


# ██████╗ ███████╗ ██████╗ ███████╗██╗  ██╗
# ██╔══██╗██╔════╝██╔════╝ ██╔════╝╚██╗██╔╝
# ██████╔╝█████╗  ██║  ███╗█████╗   ╚███╔╝
# ██╔══██╗██╔══╝  ██║   ██║██╔══╝   ██╔██╗
# ██║  ██║███████╗╚██████╔╝███████╗██╔╝ ██╗
# ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝


def matches_pattern(pattern: str, text: str, ) -> bool:
    """
    Check if a string matches a given regex pattern.

    Args:
        text (str): The string to test.
        pattern (str): The regex pattern to match against.

    Returns:
        bool: True if the string matches the pattern, False otherwise.
    """
    return bool(re.match(pattern, text))


def regex_search(pattern: str, text: str) -> str | None:
    """
    Search for a regex pattern in a string and return the matched text.

    Args:
        pattern (str): Regex pattern as a string.
        text (str): Text to search in.

    Returns:
        str | None: The matched string, or None if no match is found.
    """
    match = re.search(pattern, text)
    return match.group(0) if match else None


#  ██████╗██╗     ███████╗ █████╗ ███╗   ██╗
# ██╔════╝██║     ██╔════╝██╔══██╗████╗  ██║
# ██║     ██║     █████╗  ███████║██╔██╗ ██║
# ██║     ██║     ██╔══╝  ██╔══██║██║╚██╗██║
# ╚██████╗███████╗███████╗██║  ██║██║ ╚████║
#  ╚═════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝


def sanitize_text(text: str) -> str:
    """
    Remove all non-alphanumeric characters (except spaces) from a string.

    Args:
        text (str): Input string to sanitize.

    Returns:
        str: Sanitized string containing only letters, numbers, and spaces.
    """
    return re.sub(r'[^a-zA-Z0-9\s]', '', text)


# ███████╗███████╗ ██████╗ ███╗   ███╗███████╗███╗   ██╗████████╗
# ██╔════╝██╔════╝██╔════╝ ████╗ ████║██╔════╝████╗  ██║╚══██╔══╝
# ███████╗█████╗  ██║  ███╗██╔████╔██║█████╗  ██╔██╗ ██║   ██║
# ╚════██║██╔══╝  ██║   ██║██║╚██╔╝██║██╔══╝  ██║╚██╗██║   ██║
# ███████║███████╗╚██████╔╝██║ ╚═╝ ██║███████╗██║ ╚████║   ██║
# ╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝


def get_string_segment(string: str, split_char: str, i: int) -> str | None:
    """
    Extract a specific segment from a string.

    Args:
        string (str): The string to parse.
        split_char (str): The character used to split the string.
        i (int): The index of the path segment to retrieve (0-based).

    Returns:
        str | None: The segment at the given index, or None if it doesn't exist.
    """
    path_segments = urlparse(string).path.split(split_char)
    if 0 <= i < len(path_segments):
        return path_segments[i]
    return None
