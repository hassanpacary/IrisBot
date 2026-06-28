"""SQLite database manager.

Provides a reusable DatabaseManager class that wraps aiosqlite.
Queries are loaded from .sql files annotated with `-- name: <query_name>`
comments. Then executed by name via execute(), fetchone(), and fetchall().

© by hassanpacary
"""

# --- Standard library ---
from pathlib import Path
from sqlite3 import Row
from typing import Iterable

# --- Third-party ---
import aiosqlite

# --- Internal ---
from bot.config import regex_config
from bot.utils import strings_utils

# --- Constants ---
_DATA_DIR = Path("data")
_QUERIES_DIR = _DATA_DIR / "queries"


class DatabaseManager:
    """Manages an aiosqlite connection and a registry of named SQL queries.

    Attributes:
        db_path: Filename of the SQLite database (e.g. 'color.db').
        queries: Mapping query names to SQL queries.
        conn: Connection to the aiosqlite connection.
    """

    def __init__(self, db_path: str) -> None:
        self.db_path = _DATA_DIR / db_path
        self.queries: dict[str, str] = {}
        self.conn: aiosqlite.Connection | None = None

    # --- Connection ---

    async def connect(self) -> None:
        """Opens the aiosqlite connection to the database."""
        self.conn = await aiosqlite.connect(self.db_path)

    async def close(self) -> None:
        """Closes the aiosqlite connection cleanly."""
        if self.conn is not None:
            await self.conn.close()
            self.conn = None

    # --- Query loading ---

    def load_queries(self, filename: str) -> None:
        """Loads and indexes named SQL queries from a .sql file.

        Queries are annotated with a `-- name: <query_name>` comment
        immediately before the SQL statement.

        Args:
            filename: The .sql filename to load (e.g. 'colors.sql').
        """
        path = Path(_QUERIES_DIR) / filename
        sql = path.read_text(encoding="utf-8")
        self.queries = strings_utils.get_all_string_segments(
            string=sql,
            split_regex=regex_config.DB_QUERY_NAME_PATTERN
        )

    def get_query(self, name: str) -> str:
        """Returns the SQL query string registered under the given name.

        Args:
            name: The query name as defined in the .sql file.

        Returns:
            The SQL query string.
        """
        return self.queries[name]

    # --- Query execution ---

    async def execute(self, query_name: str, *params) -> None:
        """Executes a named SQL statement and commits the transaction.

        Args:
            query_name: The name of the query to execute.
            *params: Positional parameters to bind to the query.

        Raises:
            AssertionError: If the database is not connected.
        """
        assert self.conn is not None, "Database is not connected, call connect() first."
        await self.conn.execute(self.get_query(query_name), params)
        await self.conn.commit()

    async def fetchone(self, query_name: str, *params) -> Row | None:
        """Executes a named SQL query and returns the first result row.

        Args:
            query_name: The name of the query to execute.
            *params: Positional parameters to bind to the query.

        Returns:
            The first Row, or None if no rows match.

        Raises:
            AssertionError: If the database is not connected.
        """
        assert self.conn is not None, "Database is not connected, call connect() first."
        async with self.conn.execute(self.get_query(query_name), params) as cursor:
            return await cursor.fetchone()

    async def fetchall(self, query_name: str, *params) -> Iterable[Row]:
        """Executes a named SQL query and returns all result rows.

        Args:
            query_name: The name of the query to execute.
            *params: Positional parameters to bind to the query.

        Returns:
            A sequence of Row objects. Empty if no rows match.

        Raises:
            AssertionError: If the database is not connected.
        """
        assert self.conn is not None, "Database is not connected, call connect() first."
        async with self.conn.execute(self.get_query(query_name), params) as cursor:
            return await cursor.fetchall()
