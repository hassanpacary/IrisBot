"""Configure metadata constants for the guild cog.

Centralize the guild feature configuration and commands name - description.

© by hassanpacary
"""

# Flag for register or not the entier cog into the bot's commands tree.
ACTIVE = True


class AdminCommands:
    """Groups the admin-only features metadata constants of the guild cog."""

    class Purge:
        """Purge feature metadata constants."""

        NAME = "purge"
        DESCRIPTION = "Iris supprime tes secrets les plus sombres du salon (Défaut 1)"

        # Maximum amount of messages that can be purged.
        PURGE_AMOUNT_MAX = 100


class Itad:
    """ITAD feature metadata constants."""

    # Filter used by the ITAD API URL.
    # With this filter, we only include deals for games or bundles
    # that have a metacritic score of over 65% and are available on GOG,
    # the Humble Store, Steam, or the Epic Games Store.
    PARAMS = (
        "N4IgLgngDgpiBcBtAjAGgMwF1UgLYzAEMBVAZxgCcFRcBLAOwQDYBWHXQgDwWQAZeAv"
        "jlIALAPZRSROjboA7KiZpkTTAKA%3D"
    )

    # Dict of game store icon, based on their ITAD ID.
    STORES_ICONS = {
        "16": "https://cdn.brandfetch.io/idjxHPThVp/w/320/h/320/theme/dark/"
              "icon.jpeg?c=1bxid64Mup7aczewSAYMX&t=1767107816181",
        "35": "https://cdn.brandfetch.io/id4AgSfSM1/w/400/h/400/theme/dark/"
              "icon.png?c=1bxid64Mup7aczewSAYMX&t=1767147303131",
        "37": "https://cdn.brandfetch.io/idjNTqJgHM/w/1500/h/1500/theme/dark/"
              "icon.jpeg?c=1bxid64Mup7aczewSAYMX&t=1768894438484",
        "61": "https://cdn.brandfetch.io/idMpZmhn_O/w/400/h/400/theme/dark/"
              "icon.jpeg?c=1bxid64Mup7aczewSAYMX&t=1726566655121",
    }
