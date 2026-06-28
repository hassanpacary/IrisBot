"""Strings utilities functions.

Manage utilities functions for strings manipulation.
Like segmentation of the string.

© by hassanpacary
"""

# --- Standard library ---
import re
from urllib.parse import urlparse


def get_all_string_segments(string: str, split_regex: str) -> dict[str, str]:
    """Extracts all named segments from a string split by a regex pattern.

    Designed for parsing SQL files annotated with `-- name: <query_name>`
    comments. The regex must produce alternating (name, content) groups
    when splitting.

    Args:
        string: The full string to parse (e.g. a .sql file content).
        split_regex: A regex pattern whose capture group matches the segment name.

    Returns:
        A dict mapping each segment name to its content string.
    """
    segments: dict[str, str] = {}
    parts = re.split(split_regex, string)

    for i in range(1, len(parts), 2):
        name = parts[i]
        content = parts[i + 1].strip()
        segments[name] = content

    return segments


def get_string_segment(string: str, split_char: str, i: int) -> str:
    """Extracts a specific path segment from a URL or path string.

    Parses the path component of the string and returns the segment
    at the given index after splitting on split_char.

    Args:
        string: The URL or path string to extract from.
        split_char: The character to split the path on.
        i: The index of the segment to extract. Supports negative indexing.

    Returns:
        The segment at index i, or None if the index is out of range.
    """
    segments = urlparse(string).path.split(split_char)

    if -len(segments) <= i < len(segments):
        return segments[i]
    return ""
