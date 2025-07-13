import os
from dataclasses import dataclass
from abc import ABC, abstractmethod


class IMediator(ABC):
    ''' Mediator Interface '''
    @abstractmethod
    async def send(self, command):
        pass

    @abstractmethod
    async def query(self, query):
        pass


# Commands
@dataclass
class CollectL2data:
    symbol: str
    depth: int = 200
    is_testnet: bool = True
    collection_time_min: int = 5
    collection_interval_sec: int = 1
    snapshots_path: str = os.path.join('..', 'data', 'raw_l2_snapshots.txt')


@dataclass
class PreprocessRawL2Data:
    path_to_data: str = os.path.join('..', 'data', 'raw_l2_snapshots.txt')
    path_to_result: str = os.path.join('..', 'data', 'backtestData.csv')


@dataclass
class PerformBacktestCmd:
    path_to_backtest_data: str = os.path.join('..', 'data', 'backtestData.csv')
    path_to_report_folder: str = os.path.join('..', 'report')

