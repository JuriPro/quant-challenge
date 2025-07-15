import os
from dataclasses import dataclass
from abc import ABC, abstractmethod


class IMediator(ABC):
    """ Mediator Interface """

    @abstractmethod
    async def send(self, command):
        pass

    @abstractmethod
    async def query(self, query):
        pass


class Validatable:
    def validate(self):
        for field in self.__dataclass_fields__:
            value = getattr(self, field)
            if value is None:
                raise ValueError(f"Field '{field}' cannot be None")
        # Additional per-field checks can be added in subclasses


@dataclass
class CollectL2data(Validatable):
    symbol: str
    depth: int = 200
    is_testnet: bool = True
    collection_time_min: int = 5
    collection_interval_sec: int = 1
    snapshots_path: str = os.path.join('..', 'data', 'raw_l2_snapshots.txt')

    def validate(self):
        super().validate()
        if not isinstance(self.symbol, str) or not self.symbol:
            raise ValueError("symbol must be a non-empty string")
        if not isinstance(self.depth, int) or self.depth <= 0:
            raise ValueError("depth must be a positive integer")
        if not isinstance(self.collection_time_min, int) or self.collection_time_min <= 0:
            raise ValueError("collection_time_min must be a positive integer")
        if not isinstance(self.collection_interval_sec, int) or self.collection_interval_sec <= 0:
            raise ValueError("collection_interval_sec must be a positive integer")


@dataclass
class PreprocessRawL2Data(Validatable):
    path_to_data: str = os.path.join('..', 'data', 'raw_l2_snapshots.txt')
    path_to_result: str = os.path.join('..', 'data', 'backtestData.csv')

    def validate(self):
        super().validate()
        if not isinstance(self.path_to_data, str) or not self.path_to_data:
            raise ValueError("path_to_data must be a non-empty string")
        if not isinstance(self.path_to_result, str) or not self.path_to_result:
            raise ValueError("path_to_result must be a non-empty string")


@dataclass
class PerformBacktestCmd(Validatable):
    delta_jump_level: float = 15
    path_to_backtest_data: str = os.path.join('..', 'data', 'backtestData.csv')
    path_to_report_folder: str = os.path.join('..', 'report')

    def validate(self):
        super().validate()
        if not isinstance(self.delta_jump_level, (float, int)):
            raise ValueError("delta_jump_level must be a float or int")
        if not isinstance(self.path_to_backtest_data, str) or not self.path_to_backtest_data:
            raise ValueError("path_to_backtest_data must be a non-empty string")
        if not isinstance(self.path_to_report_folder, str) or not self.path_to_report_folder:
            raise ValueError("path_to_report_folder must be a non-empty string")
