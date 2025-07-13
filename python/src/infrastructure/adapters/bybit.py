import sys
import asyncio
import aiohttp
import numpy as np


class BybitClient:
    """Клиент Bybit, чо. Тянем ордербук и считаем дельту."""

    BASE_URL = "https://api-testnet.bybit.com"

    def __init__(self) -> None:

        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        '''Causes library errors for out-of-context sessions...'''
        # self._session = aiohttp.ClientSession() # Rise

    async def fetch_orderbook_snapshot(self, symbol: str, limit: int = 200) -> dict:
        """Асинхронно получаем срез ордербука."""

        url = f"{self.BASE_URL}/v5/market/orderbook"
        params = {"category": "linear", "symbol": symbol, "limit": limit}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params, timeout=5) as resp:
                    data = await resp.json()
                    return data.get("result", {})
            except aiohttp.ClientError as e:
                print(f"Client error: {e}")
            except asyncio.TimeoutError:
                print("Request timed out")

    async def close(self) -> None:
        """Закрываем сессию aiohttp."""
        await self._session.close()
