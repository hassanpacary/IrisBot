"""Configure metadata constants for the fun cog.

Centralize the fun feature configuration and commands name - description.

© by hassanpacary
"""

# Flag for register or not the entier cog into the bot's commands tree.
ACTIVE = True


class Quoi:
    """quoi feature metadata constants."""

    NAME = "quoi"
    DESCRIPTION = "Répond 'feur'"


class Quote:
    """Quote feature metadata constants."""

    NAME = "quote"
    DESCRIPTION = "Expose un utilisateur grâce à une capture d'écran (requise)"
    CONTEXT_MENU = "Quote"

    # Reset time for the monthly quote festival.
    # The festival resets on the first of every month at 6 p.m.
    QUOTE_FEST_RESET_HOUR = 18
    QUOTE_FEST_RESET_MINUTE = 0

    # Reaction emoji user can use for quote user by the payload.
    REACTION_FOR_QUOTE = "📸"


class Roll:
    """Roll feature metadata constants."""

    NAME = "roll"
    DESCRIPTION = (
        "Lance un dés pour déterminer un nombre aléatoire... "
        "Si Iris ne pipe pas le dés (Défaut 6)"
    )


class Say:
    """Repeat feature metadata constants."""

    NAME = "say"
    DESCRIPTION = "Répète ta phrase mot pour mot"
