"""
bot/utils/aiohttp_client.py
© by hassanpacary

Reusable asynchronous HTTP client for the Bot using aiohttp.
Provides a global session, request helper methods, and automatic cleanup.
"""

# --- Imports ---
import logging
from typing import Optional, Dict, Any

# --- Third party imports ---
import aiohttp


# ██╗  ██╗████████╗████████╗██████╗      ██████╗██╗     ██╗███████╗███╗   ██╗████████╗
# ██║  ██║╚══██╔══╝╚══██╔══╝██╔══██╗    ██╔════╝██║     ██║██╔════╝████╗  ██║╚══██╔══╝
# ███████║   ██║      ██║   ██████╔╝    ██║     ██║     ██║█████╗  ██╔██╗ ██║   ██║
# ██╔══██║   ██║      ██║   ██╔═══╝     ██║     ██║     ██║██╔══╝  ██║╚██╗██║   ██║
# ██║  ██║   ██║      ██║   ██║         ╚██████╗███████╗██║███████╗██║ ╚████║   ██║
# ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝          ╚═════╝╚══════╝╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝


class AioHttpClient:
    """Singleton-like async HTTP client for reusing a single aiohttp.ClientSession."""

    _session: Optional[aiohttp.ClientSession] = None

    def __init__(self, headers: Optional[Dict[str, str]] = None, timeout: int = 10):
        """Initialize the HTTP client with optional default headers and timeout."""
        self._headers = headers or {}
        self._timeout = aiohttp.ClientTimeout(total=timeout)

    @property
    def session(self) -> aiohttp.ClientSession:
        """
        Return the singleton aiohttp.ClientSession.

        If the session does not exist or is closed, creates a new one
        using the default headers and timeout.

        Returns:
            aiohttp.ClientSession: The active client session.
        """
        if not self._session or self._session.closed:
            self._session = aiohttp.ClientSession(headers=self._headers, timeout=self._timeout)

        return self._session

    #  ██████╗ ███████╗████████╗     █████╗ ███╗   ██╗██████╗     ██████╗  ██████╗ ███████╗████████╗
    # ██╔════╝ ██╔════╝╚══██╔══╝    ██╔══██╗████╗  ██║██╔══██╗    ██╔══██╗██╔═══██╗██╔════╝╚══██╔══╝
    # ██║  ███╗█████╗     ██║       ███████║██╔██╗ ██║██║  ██║    ██████╔╝██║   ██║███████╗   ██║
    # ██║   ██║██╔══╝     ██║       ██╔══██║██║╚██╗██║██║  ██║    ██╔═══╝ ██║   ██║╚════██║   ██║
    # ╚██████╔╝███████╗   ██║       ██║  ██║██║ ╚████║██████╔╝    ██║     ╚██████╔╝███████║   ██║
    #  ╚═════╝ ╚══════╝   ╚═╝       ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝     ╚═╝      ╚═════╝ ╚══════╝   ╚═╝

    async def get(self, url: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> aiohttp.ClientResponse:
        """
        Send an asynchronous HTTP GET request.

        Args:
            url (str): The target URL to request.
            params (Optional[Dict[str, Any]]): Query parameters to include in the request.
            **kwargs: Additional keyword arguments passed to aiohttp.ClientSession.get().

        Returns:
            aiohttp.ClientResponse: The response object from the request.

        Raises:
            aiohttp.ClientError: If the request fails (connection issues, timeout, etc.).
        """
        try:
            resp = await self.session.get(url, params=params, **kwargs)
            resp.raise_for_status()
            return resp

        except aiohttp.ClientError as e:
            logging.error(f"GET request failed: {url}.\n{e}")
            raise

    async def post(self, url: str, json: Optional[Dict[str, Any]] = None, data: Any = None,
                   **kwargs) -> aiohttp.ClientResponse:
        """
        Send an asynchronous HTTP POST request.

        Args:
            url (str): The target URL to request.
            json (Optional[Dict[str, Any]]): JSON data to send in the body of the request.
            data (Any): Optional raw data to send instead of JSON.
            **kwargs: Additional keyword arguments passed to aiohttp.ClientSession.post().

        Returns:
            aiohttp.ClientResponse: The response object from the request.

        Raises:
            aiohttp.ClientError: If the request fails (connection issues, timeout, etc.).
        """
        try:
            resp = await self.session.post(url, json=json, data=data, **kwargs)
            resp.raise_for_status()
            return resp

        except aiohttp.ClientError as e:
            logging.error(f"POST request failed: {url}.\n{e}")
            raise

    #  █████╗  ██████╗████████╗██╗ ██████╗ ███╗   ██╗███████╗
    # ██╔══██╗██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝
    # ███████║██║        ██║   ██║██║   ██║██╔██╗ ██║███████╗
    # ██╔══██║██║        ██║   ██║██║   ██║██║╚██╗██║╚════██║
    # ██║  ██║╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║███████║
    # ╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝

    async def download_bytes(self, url: str, **kwargs) -> bytes | None:
        """
        Download the raw bytes from a given URL.

        Args:
            url (str): The URL to download.
            **kwargs: Additional arguments passed to aiohttp.ClientSession.get().

        Returns:
            bytes | None: The raw content if the download succeeded, None otherwise.
        """
        try:
            async with self.session.get(url, **kwargs) as resp:
                if resp.status == 200:
                    return await resp.read()

                logging.warning(f"Failed to download bytes from {url} (status {resp.status})")
                return None

        except aiohttp.ClientError as e:
            logging.error(f"Download request failed: {url}.\n{e}")
            return None

    async def close(self):
        """
        Close the aiohttp.ClientSession cleanly.

        Should be called when the bot shuts down to release resources.

        Example:
            await aiohttp_client.close()
        """
        if self._session and not self._session.closed:
            await self._session.close()


# --- Singleton instance for global usage ---
aiohttp_client = AioHttpClient(headers={"Content-Type": "application/json"})


async def aiohttp_shutdown():
    """
    Convenience function to close the global aiohttp_client session.

    Can be called from the bot shutdown hook to ensure proper cleanup.

    Example:
        await shutdown()
    """
    await aiohttp_client.close()
