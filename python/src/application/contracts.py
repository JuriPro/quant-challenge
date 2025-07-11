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
class CalculateDeltaMetric:
    prev_snapshot: dict
    curr_snapshot: dict

@dataclass
class ProcessRawL2Data:
    path_to_data: str
    path_to_result: str

@dataclass
class PerformBacktest:
    path_to_data: str
    path_to_report: str

