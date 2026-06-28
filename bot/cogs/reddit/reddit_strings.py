"""Text strings constants for reddit cog.

Centralizes bot response or simple labels used by reddit features.
Strings with placeholders use `str.format` syntax.

© by hassanpacary
"""

# Waf command executed successfully or Reddit URL is listened in one user message.
RESPONSE = "Voilà toutes les informations du post Reddit 🐷"

# Response to user of the URL of the waf command not matched with Reddit URL pattern.
WRONG_URL = "C'est le lien d'un post Reddit pour toi ça ?"

class RedditEmbedFields:
    """Strings used by the Reddit feature.
    Used for construct the improved embed message."""

    AUTHOR = "Auteur"
    FOOTER = "Reddit"
    RESPONSES = "Réponses"
    UPVOTE = "Upvote"
