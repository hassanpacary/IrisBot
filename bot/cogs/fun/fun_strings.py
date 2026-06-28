"""Text strings constants for fun cog.

Centralizes bot response or simple labels used by fun features.
Strings with placeholders use `str.format` syntax.

© by hassanpacary
"""

# Quoi command executed successfully.
QUOI_RESPONSE = "feur"

# Roll command executed successfully.
ROLL_RESULT = "Laisse moi réfléchir ... {result} !"


class Quote:
    """Strings used by the quote feature."""

    # Quote command executed successfully.
    HANDLE_QUOTE_RESPONSE = "Pris en flagrant délit — *Eh-Nah* 📸"

    # Embed labels
    START_QUOTE = "*— \""
    END_QUOTE = "\"*"
    DISCLOSER_MEMBER = "Divulgé par :"
    QUOTED_USER = "Pris en flagrant délit :"
    FOOTER = "wbz citation fest"

    # End of quote Fest result message send in quote channel.
    MONTH_RESULT = (
        "**Fin des festivités de {month} !**\n\n"
        "Bravo à {discloser} pour avoir montré une nouvelle facette de {author} "
        "que l'on ignorait tous 🦧"
    )


class Say:
    """Strings used by the repeat feature."""

    # Repeat command executed successfully (ephemeral).
    WITH_SUCCESS = "Tout a été répété mot pour mot 🐕‍🦺"

    # Repeat command executed successfully and disclose the user who use it.
    WITH_SOURCE = "Tout a été répété d'après les mots de {user}"
