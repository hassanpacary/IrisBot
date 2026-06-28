"""Configuration regex pattern constants.

© by hassanpacary
"""

DB_QUERY_NAME_PATTERN = r"--\s*name:\s*(\w+)"
QUOI_FEUR = r"^.*quoi\s*[?!.]*\s*$"
REDDIT_URL = r"(https?://(?:www\.)?reddit\.com/r/\w+/comments/[A-Za-z0-9]+/\S+)"
HEX_COLOR_VALUE = r"^(?:#)?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
YOUTUBE_URL = (
        r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(?:-nocookie)?\.com|youtu"
        r".be))(\/(?:[\w\-]+\?v=|embed\/|live\/|v\/)?)([\w\-]+)(\S+)?$"
    )
