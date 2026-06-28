"""Strings constants related to the social cog.

© by hassanpacary
"""


class AvatarEmbedFields:
    """Groups strings constants related to the avatar embed label."""

    AUTHOR = "Avatar de {user}"

class Color:
    """Groups strings constants related to the color command."""

    WITH_SUCCESS = "Nouvelle couleur assignée. Tu es tout beau !"
    CREATE_REASON = "Modification de la couleur par le biais d'Iris"
    DELETE_REASON = "Suppression de l'ancienne couleur par le biais d'Iris"
    INVALID_HEX = "Euh, ce n'est pas un code couleur HEX ça ☝️🤓"
    LEVEL_NOT_REACHED = (
        "Continu de discuter avec les autres avant que je fasse "
        "ça pour toi"
    )

class ProfileCard:
    """Groups strings constants related to the profile card."""

    NO_PROFILE = "Je peux savoir qui tu es ?"
    LEVEL_LABEL = "L     E     V     E     L        {level}"
    XP_LABEL = "{xp} / {next_level}"
