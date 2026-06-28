"""Configure metadata constants for the social cog.

Centralize the social feature configuration and commands name - description.

© by hassanpacary
"""

# Flag for register or not the entier cog into the bot's commands tree.
ACTIVE = True


class Avatar:
    """Avatar feature metadata constants."""

    NAME = "avatar"
    DESCRIPTION = (
        "Envoie l'avatar d'un membre du serveur "
        "(ton avatar si aucun membre mentionné)"
    )


class Color:
    """Color feature metadata constants."""

    NAME = "color"
    DESCRIPTION = "Choisis ta propre couleur"

    # Required level for use custom color feature.
    LEVEL_FOR_USE_COLOR_COMMAND = 3

    # Role ID for move created custom role in guild roles list.
    COLOR_ROLE_ID_POSITION = 1471313232651358218


class Profile:
    """Profile feature metadata constants."""

    NAME = "profile"
    DESCRIPTION = "Affiche ton profil ou celui d'un autre membre du serveur"
