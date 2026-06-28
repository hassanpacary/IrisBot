"""Configure metadata constants for the level cog.

Centralize the level feature configuration and commands name - description.

© by hassanpacary
"""

# Flag for register or not the entier cog into the bot's commands tree.
ACTIVE = True

# Maximum amount of XP that can be awarded to a user for each message sent.
# Random amount: 1 to RANDOM_XP_MAX.
RANDOM_XP_MAX = 3

# Multiplier used in the formula to calculate the amount of XP the user will need
# to level up.
XP_PER_LEVEL_MULTIPLIER = 25


class Leaderboard:
    """Leaderboard feature metadata constants."""

    NAME = "leaderboard"
    DESCRIPTION = "Classements par level et experience des membres du discord"

    # Number of users in each page of the leaderboard.
    LEADERBOARD_PAGE_SIZE = 10


class AdminCommands:
    """Groups the admin-only features metadata constants of the level cog."""

    class Give:
        """Give feature metadata constants."""

        NAME = "give"
        DESCRIPTION = "Give de l'expérience à un utilisateur"

    class Reset:
        """Reset feature metadata constants."""

        NAME = "reset"
        DESCRIPTION = "Remets à zéro les levels d'un utilisateur"
