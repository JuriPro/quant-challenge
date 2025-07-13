import json
import logging
import asyncio
import datetime as dt
import pandas as pd

from application.contracts import *
from application.helpers import SnapshotCalc
from infrastructure.adapters.bybit import BybitClient

from backtesting import Strategy
from backtesting import Backtest
from application.strategy import OrderBookStrategy, save_strategy_result


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

        log.info(
            f"Collecting L2 data for {command.symbol}, with interval {command.collection_interval_sec} is finished!")

        return f"The Data was successfully collected and stored in {command.snapshots_path}"


class PreprocessBacktestData:
    async def handle(self, command: PreprocessRawL2Data):
        log.info(f"Start preprocessing Data for Backtest from {command.path_to_data}...")

        delta = None
        prev_snapshot = None
        backtest_data = {'timestamp': [], 'mid_price': [], 'delta': []}

        file_path = command.path_to_data
        with open(file_path, 'r') as file:
            for snapshot in file:
                curr_snapshot = json.loads(snapshot)
                mid_price = SnapshotCalc.calculate_mid_price(curr_snapshot)

                if prev_snapshot:
                    delta = SnapshotCalc.calculate_delta(curr_snapshot, prev_snapshot)

                backtest_data['timestamp'].append(int(curr_snapshot['ts']))
                backtest_data['mid_price'].append(mid_price)
                backtest_data['delta'].append(delta)

                prev_snapshot = curr_snapshot

        l2_df = pd.DataFrame(data=backtest_data, columns=['timestamp', 'mid_price', 'delta'])

        l2_df = l2_df.assign(
            Open=l2_df['mid_price'], High=l2_df['mid_price'], Low=l2_df['mid_price'], Close=l2_df['mid_price'])

        l2_df['timestamp'] = pd.to_datetime(l2_df['timestamp'], unit='ms')

        l2_df.to_csv(command.path_to_result, index=False)

        log.info(f"Preprocessing successfully finished, target file: {command.path_to_result}")
        
        return command.path_to_result


class PerformBacktest:
    async def handle(self, command: PerformBacktestCmd):
        log.info(f"Start strategy Backtesting...")
        
        backtest_df = pd.read_csv(command.path_to_backtest_data)
        backtest_df['timestamp'] = pd.to_datetime(backtest_df['timestamp'])
        backtest_df.set_index(backtest_df['timestamp'], inplace=True, drop=True)
        
        bt = Backtest(backtest_df, OrderBookStrategy, cash=100000, commission=.002, exclusive_orders=True, finalize_trades=True)
        stats = bt.run()
        
        print_result = save_strategy_result(stats, save_folder_path=command.path_to_report_folder)
        
        log.info(f"Backtest is finished...")

        return stats
