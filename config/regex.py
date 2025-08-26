import re

# Regex for quoi - feur event
FUN_QUOIFEUR_REGEX = re.compile(r'^(.*?(\bquoi\b)[^$]*)$', re.IGNORECASE)

# Regex for detect reddit link
REDDIT_URL_REGEX = re.compile(r'(https?://(?:www\.)?reddit\.com/r/\w+/comments/[A-Za-z0-9]+/\S+)')