"""AniList GraphQL API requests.

Fetches anime metadata from the AniList GraphQL API using the gql library.

Each request opens a new authenticated transport session and closes it cleanly
after the query completes.

Used by actvity service for pick a random anime for set the bot's Discord presence.

© by hassanpacary
"""

# --- Standard library ---
import logging
import random
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, AsyncGenerator

# --- Third-party ---
from aiohttp import ClientError
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import (
    TransportQueryError,
    TransportServerError,
    TransportProtocolError,
    TransportError,
)
from graphql import build_ast_schema, parse

# --- Constants ---
_ANILIST_API_URL: str = "https://graphql.anilist.co"
_ANILIST_HEADERS: dict = {"Content-Type": "application/json"}
_QUERIES_DIR: Path = Path("api") / "anilist" /"queries"


@asynccontextmanager
async def _open_session() -> AsyncGenerator[Any, Any]:
    """Opens an authenticated AniList GraphQL session via aiohttp transport.

    Builds the transport from the AniList endpoint and validates queries
    against the local GraphQL schema before execution.

    Yields:
        An active gql.Client session ready to execute queries against AniList.

    Raises:
        TransportError: If the connection to AniList cannot be established.
        FileNotFoundError: If the local schema.graphql file is missing.
    """
    try:
        transport = AIOHTTPTransport(
            url=_ANILIST_API_URL,
            headers=_ANILIST_HEADERS,
        )
        schema = build_ast_schema(parse((_QUERIES_DIR / "schema.graphql").read_text()))

        async with Client(transport=transport, schema=schema) as session:
            yield session
    except TransportError as e:
        logging.error(
            "Connection to AniList GraphQL API can't be established: %s.",
            e,
        )
        raise
    except FileNotFoundError as e:
        logging.error(
            "GraphQL schema can't be validate or missing: %s.",
            e,
        )
        raise


async def _get_total_anime_count() -> int:
    """Fetches the total number of anime entries indexed by AniList.

    Used to calculate the maximum valid page number before picking
    a random page in fetch_random_anime().

    Returns:
        The total anime count as reported by the AniList pageInfo.

    Raises:
        TransportQueryError: If AniList rejects the query.
        TransportServerError: If AniList returns a server-side error.
        ClientError: If the HTTP connection fails.
        FileNotFoundError: If the query .graphql file is missing.
    """
    query = gql((_QUERIES_DIR / "get_anilist_total_anime.graphql").read_text())

    try:
        async with _open_session() as session:
            resp = await session.execute(query)
        return resp["Page"]["pageInfo"]["total"]
    except (
        TransportQueryError,
        TransportServerError,
        TransportProtocolError,
        TransportError,
        ClientError,
        FileNotFoundError,
    ) as e:
        logging.error(
            "AniList API request for getting total anime count failed: %s.",
            e,
        )
        raise


# --- Exposed functions ---


async def fetch_random_anime() -> dict:
    """Fetches a random anime entry from the AniList API.

    AniList paginates its anime catalogue. This function first fetches
    the total anime count to calculate the maximum page number, then selects
    a random page and returns a random entry from that page's results.

    Returns:
        A dict of anime metadata.

    Raises:
        TransportQueryError: If AniList rejects the query.
        TransportServerError: If AniList returns a server-side error.
        ClientError: If the HTTP connection fails.
        FileNotFoundError: If a query .graphql file is missing.
    """
    query = gql((_QUERIES_DIR / "get_anilist_random_page.graphql").read_text())

    total_animes = await _get_total_anime_count()
    max_pages = (total_animes // 25) + 1 # 25 is the number of anime per pages.
    random_page = random.randint(1, max_pages)

    try:
        async with _open_session() as session:
            resp = await session.execute(
                query,
                variable_values={"page": random_page, "perPage": 25},
            )
        return random.choice(resp["Page"]["media"])
    except (
        TransportQueryError,
        TransportServerError,
        TransportProtocolError,
        TransportError,
        ClientError,
        FileNotFoundError,
    ) as e:
        logging.error(
            "AniList API request for getting a random anime failed: %s.",
            e,
        )
        raise
