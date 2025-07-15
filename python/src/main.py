import os
import logging
import asyncio
from logging.handlers import RotatingFileHandler
from typing import Any

from CONFIG import cfg

# CQRS support
from application.handlers import *
from application.mediator import Mediator


def setup_logging() -> logging.Logger:
    log_dir = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(log_dir, "info.log")

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Rotating handler for log files
    file_handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=3, encoding='utf-8')
    stream_handler = logging.StreamHandler()

    formatter = logging.Formatter("%(asctime)s %(levelname)s :: %(message)s")
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


async def collect_l2_data(mediator: Mediator, logger: logging.Logger) -> Any:
    if not cfg.get('use_previous_data', False):
        try:
            result = await mediator.send(
                CollectL2data(
                    symbol=cfg['symbol'],
                    depth=cfg['depth'],
                    collection_time_min=cfg['collection_time_min'],
                    collection_interval_sec=cfg['collection_interval_sec']
                )
            )
            logger.info(result)
            return result
        except Exception as e:
            logger.error(f"Error collecting L2 data: {e}", exc_info=True)
            raise


async def preprocess_data(mediator: Mediator, logger: logging.Logger) -> Any:
    try:
        fpath = await mediator.send(PreprocessRawL2Data())
        logger.info(f"Preprocessed data file path: {fpath}")
        return fpath
    except Exception as e:
        logger.error(f"Error preprocessing backtest data: {e}", exc_info=True)
        raise


async def perform_backtest(mediator: Mediator, logger: logging.Logger) -> Any:
    try:
        report = await mediator.send(PerformBacktestCmd())
        logger.info(f"\n\nBacktest result:\n\n{report}")
        return report
    except Exception as e:
        logger.error(f"Error performing backtest: {e}", exc_info=True)
        raise


async def main():
    logger = setup_logging()
    logger.info("--- START ---")
    try:
        mediator = Mediator()

        # Register handlers
        handler_mappings = [
            (CollectL2data, CollectL2DataHandler()),
            (PreprocessRawL2Data, PreprocessBacktestData()),
            (PerformBacktestCmd, PerformBacktest()),
        ]
        for cmd, handler in handler_mappings:
            mediator.register_command_handler(cmd, handler)

        # Run pipeline
        if not cfg.get('use_previous_data', False):
            await collect_l2_data(mediator, logger)

        await preprocess_data(mediator, logger)
        await perform_backtest(mediator, logger)

    except Exception as e:
        logger.critical(f"Unhandled exception in main: {e}", exc_info=True)
        raise
    finally:
        logger.info("--- END ---")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.critical(f"Fatal error running main: {e}", exc_info=True)
