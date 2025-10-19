"""
bot/utils/db_manager.py
© by hassanpacary

Manager for db
"""

# --- Imports ---
import os
import pathlib

# --- Third party imports ---
import aiosqlite

# --- Bot modules ---
from bot.core.config_loader import REGEX
from bot.utils.strings_utils import get_string_segments


# ██████╗ ██████╗     ███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗██████╗
# ██╔══██╗██╔══██╗    ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗
# ██║  ██║██████╔╝    ██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝
# ██║  ██║██╔══██╗    ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██╔══██╗
# ██████╔╝██████╔╝    ██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║
# ╚═════╝ ╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝


class DatabaseManager:
    """Manager class for db"""

    def __init__(self, db_path: str):
        """Initialize the db"""
        self.db_path = os.path.join("bot", "database", db_path)
        self.queries_path = os.path.join("bot", "database", "queries")
        self.queries: dict[str, str] = {}
        self.conn: aiosqlite.Connection | None = None

    #  ██████╗ ██████╗ ███╗   ██╗███╗   ██╗
    # ██╔════╝██╔═══██╗████╗  ██║████╗  ██║
    # ██║     ██║   ██║██╔██╗ ██║██╔██╗ ██║
    # ██║     ██║   ██║██║╚██╗██║██║╚██╗██║
    # ╚██████╗╚██████╔╝██║ ╚████║██║ ╚████║
    #  ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝

    async def connect(self):
        """Connect to the database"""
        self.conn = await aiosqlite.connect(self.db_path)
        await self.conn.execute("PRAGMA foreign_keys = ON;")
        await self.conn.commit()

    async def close(self):
        """Close the connection"""
        if self.conn:
            await self.conn.close()

    # ██╗   ██╗████████╗██╗██╗     ███████╗
    # ██║   ██║╚══██╔══╝██║██║     ██╔════╝
    # ██║   ██║   ██║   ██║██║     ███████╗
    # ██║   ██║   ██║   ██║██║     ╚════██║
    # ╚██████╔╝   ██║   ██║███████╗███████║
    #  ╚═════╝    ╚═╝   ╚═╝╚══════╝╚══════╝

    def load_queries(self, filename: str):
        """Load queries from .sql file and index all requests by their name"""
        queries_path = pathlib.Path(self.queries_path)
        path = queries_path / filename
        sql = path.read_text(encoding="utf-8")

        pattern = REGEX['database']['pattern']
        self.queries = get_string_segments(string=sql, split_regex=pattern)

    def get_query(self, name: str) -> str:
        return self.queries[name]

    #  ██████╗ ██╗   ██╗███████╗██████╗ ██╗███████╗███████╗
    # ██╔═══██╗██║   ██║██╔════╝██╔══██╗██║██╔════╝██╔════╝
    # ██║   ██║██║   ██║█████╗  ██████╔╝██║█████╗  ███████╗
    # ██║▄▄ ██║██║   ██║██╔══╝  ██╔══██╗██║██╔══╝  ╚════██║
    # ╚██████╔╝╚██████╔╝███████╗██║  ██║██║███████╗███████║
    #  ╚══▀▀═╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝

    async def execute(self, query_name: str, *params):
        """Execute a query and return the result"""
        assert self.conn, "Database not connected"
        await self.conn.execute(self.get_query(query_name), params)
        await self.conn.commit()

    async def fetchone(self, query_name: str, *params):
        """Fetch the result of a query and return the result"""
        assert self.conn, "Database not connected"
        async with self.conn.execute(self.get_query(query_name), params) as cursor:
            return await cursor.fetchone()

    async def fetchall(self, query_name: str, *params):
        """Fetch the result of a query and return the result"""
        assert self.conn, "Database not connected"
        async with self.conn.execute(self.get_query(query_name), params) as cursor:
            return await cursor.fetchall()
