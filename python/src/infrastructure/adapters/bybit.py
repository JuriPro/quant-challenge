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

    async def calculate_delta(self, snapshot_prev: dict, snapshot_new: dict) -> float:
        """Высчитываем дельту между снапшотами."""
        bids_prev = np.array(snapshot_prev.get("b", []), dtype=float)
        asks_prev = np.array(snapshot_prev.get("a", []), dtype=float)
        bids_new = np.array(snapshot_new.get("b", []), dtype=float)
        asks_new = np.array(snapshot_new.get("a", []), dtype=float)

        delta_prev = bids_prev[:, 1].sum() - asks_prev[:, 1].sum() if bids_prev.size and asks_prev.size else 0.0
        delta_new = bids_new[:, 1].sum() - asks_new[:, 1].sum() if bids_new.size and asks_new.size else 0.0
        return float(delta_new - delta_prev)

    async def close(self) -> None:
        """Закрываем сессию aiohttp."""
        await self._session.close()
