"""Configure metadata constants for the reddit cog.

Centralize the reddit feature configuration and commands name - description.

© by hassanpacary
"""

# Flag for register or not the entier cog into the bot's commands tree.
ACTIVE = True


class Waf:
    """waf feature metadata constants."""

    NAME = "waf"
    DESCRIPTION = (
        "Répond en envoyant un meilleur embed pour le post reddit, "
        "suivis par les différents médias du post"
    )
