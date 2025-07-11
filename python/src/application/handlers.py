import json
import logging
import asyncio
import datetime as dt

from application.contracts import *
from infrastructure.adapters.bybit import BybitClient

log = logging.getLogger()


class CollectL2DataHandler:
    async def handle(self, command: CollectL2data):
        log.info(f"Start collecting order book data: Wait {command.collection_time_min} minutes...")

        client = BybitClient()

        time_of_completion = dt.datetime.now() + dt.timedelta(minutes=command.collection_time_min)
        while dt.datetime.now() <= time_of_completion:
            snapshot = await client.fetch_orderbook_snapshot(symbol=command.symbol)

            with open(command.snapshots_path, 'a', encoding='utf-8') as f:
                json.dump(snapshot, f, ensure_ascii=False)
                f.write('\n')

            await asyncio.sleep(command.collection_interval_sec)

        log.info(f"Collecting L2 data for {command.symbol}, with interval {command.collection_interval_sec} is finished!")

        return f"The Data was successfully collected and stored in {command.snapshots_path}"
