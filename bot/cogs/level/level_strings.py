"""Text strings constants for level cog.

Centralizes bot response or simple labels used by level features.
Strings with placeholders use `str.format` syntax.

© by hassanpacary
"""

# Event message sent if user level up.
LEVEL_UP = "{user} vient de passer niveau {level} !"

# Give command executed successfully.
GIVE_XP = (
    "{amount} points d'expérience viennent d'être gracieusement donnés "
    "à {user}"
)

# Reset command executed successfully.
LEVEL_RESET = "Les niveaux de {user} on bien étés remis à zéro !"

# Response to the admin who want to reset a specific user,
# if this user is not in the bot DB.
MEMBER_NOT_IN_DB = "Le membre n'existe pas"


class Leaderboard:
    """Strings used by the leaderboard feature.
    Used for construct the Leaderboard view."""

    BUTTON_NEXT = "➡️ Suivant"
    BUTTON_PREVIOUS = "⬅️ Précédent"
    PREVENT_OTHER_MEMBER_INTERACTION = "Bouge."
    TITLE = "👑 Leaderboard — Page {current_page}/{pages}"
    UNKNOWN_USER = "unknow_user"
    USER_LEVEL_FIELD = "**Niveau :** {level} | **XP :** {xp}/{next_level}"
    USER_NAME_FIELD = "{rank} — {display_name}"
