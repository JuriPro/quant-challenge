import numpy as np


class SnapshotCalc:
    @staticmethod
    def calculate_mid_price(snapshot: dict):
        """Calculate mid price for Backtest"""
        bids = np.array(snapshot.get("b", []), dtype=float)
        asks = np.array(snapshot.get("a", []), dtype=float)

        best_bid = bids[:, 0].max() if bids.size else 0.0
        best_ask = asks[:, 0].min() if asks.size else 0.0

        mid_price = (best_bid + best_ask) / 2.0
        return mid_price

    @staticmethod
    def calculate_delta(snapshot_prev: dict, snapshot_new: dict) -> float:
        """Высчитываем дельту между снапшотами."""
        bids_prev = np.array(snapshot_prev.get("b", []), dtype=float)
        asks_prev = np.array(snapshot_prev.get("a", []), dtype=float)
        bids_new = np.array(snapshot_new.get("b", []), dtype=float)
        asks_new = np.array(snapshot_new.get("a", []), dtype=float)

        delta_prev = bids_prev[:, 1].sum() - asks_prev[:, 1].sum() if bids_prev.size and asks_prev.size else 0.0
        delta_new = bids_new[:, 1].sum() - asks_new[:, 1].sum() if bids_new.size and asks_new.size else 0.0
        return float(delta_new - delta_prev)

