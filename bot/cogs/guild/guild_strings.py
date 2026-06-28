"""Text strings constants for guild cog.

Centralizes bot response or simple labels used by guild features.
Strings with placeholders use `str.format` syntax.

© by hassanpacary
"""

# Welcome message for new member of the guild.
WELCOME_MESSAGES = [
    "Konnichiwassup {user}",
    "{user} domo 🙇‍♀️",
]

# Goodbye message for former member of the guild.
GOODBYE_MESSAGES = [
    "Seeyanara {user} 🧙‍♀️",
]

class Activity:
    """Strings used by the activity feature (bot Discord presence)."""

    # List of presets games activities.
    PRESET_GAME = [
        ("GoogooBabies Game", "Hmm mm les googoo"),
        ("Ethorn", "En maintenance depuis 2017 ..."),
    ]

    # List of presets watching activities.
    PRESET_WATCHING = [
        ("Zero no Tsukaima", "Louise my beloved <3"),
        (
            "KONOSUBA - God's blessing on this wonderful world !",
            "Darkness blacker than black and darker than dark, I beseech thee, "
            "combine with my deep crimson"
        ),
    ]

    class WatchingStateInfo:
        """Used for construct the watching state of the activity
        when the bot is watching an anime from the AniList API.
        """

        EPISODE = "episode"
        MEAN_SCORE = "score moyen"
        GENRE = "genre"
        SEPARATOR = " | "

class DealsEmbedFields:
    """Strings used by the deals feature.
    Used for construct the embed deal message.
    """

    AUTHOR = "{store}"
    DESCRIPTION = "Promotion de **{pourcent}%** jusqu'au {date}."
    DESCRIPTION_WITH_NO_DATE = (
        "Promotion de **{pourcent}%** jusqu'au *date manquante*."
    )
    HISTORY_LOW_PRICE = "{history_price}€"
    HISTORY_LOW_PRICE_LABEL = "**Prix historique**"
    NEW_PRICE = "{new_price}€"
    NEW_PRICE_LABEL = "Prix avec réduction"
    OLD_PRICE = "~~{old_price}€~~"
    OLD_PRICE_LABEL = "Prix standard"

class Logs:
    """Strings used by the logs feature.
    Used for construct the log embed message."""

    DELETED_MESSAGE = "Message supprimé"
    EDITED_MESSAGE = "Message édité"
    NEW_MESSAGE_FIELD = "Modifications"

class Purge:
    """Strings used by the purge feature."""

    # Response to the user if the amount a message is too high (ephemeral).
    AMOUNT_TOO_HIGH = (
        "Tu as tant de chose que ça à cacher ? "
        "Je ne peux pas purger plus de {max} messages"
    )

    # Response to the user if the amount a message is too low (ephemeral).
    AMOUNT_TOO_LOW = (
        "J'ai besoin d'au moins un pauvre petit message pour pouvoir le supprimer"
    )

    # Purge command executed successfully (ephemeral).
    WITH_SUCCESS = "J'ai supprimée {amount} messages"
