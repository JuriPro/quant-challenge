import os
import logging
import asyncio

from CONFIG import cfg

# CQRS support
from application.handlers import *
from application.mediator import Mediator

logging.basicConfig(
    format="%(asctime)s %(levelname)s :: %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("{path}/{fname}.log".format(path=os.path.dirname(os.path.abspath(__file__)),
                                                        fname="info"), encoding='utf-8'),
        logging.StreamHandler()
    ])

log = logging.getLogger()


async def main():
    try:
        mediator = Mediator()

        # Register handlers
        mediator.register_command_handler(CollectL2data, CollectL2DataHandler())
        mediator.register_command_handler(PreprocessRawL2Data, PreprocessBacktestData())
        mediator.register_command_handler(PerformBacktestCmd, PerformBacktest())

        # Send a command
        if not cfg['use_previous_data']:
            try:
                collect_l2_result = await mediator.send(
                    CollectL2data(symbol=cfg['symbol'],
                                  depth=cfg['depth'],
                                  collection_time_min=cfg['collection_time_min'],
                                  collection_interval_sec=cfg['collection_interval_sec']))
                log.info(collect_l2_result)
            except Exception as e:
                log.error(f"Error collecting L2 data: {e}", exc_info=True)

        try:
            backtest_data_fpath = await mediator.send(PreprocessRawL2Data())
            log.info(backtest_data_fpath)
        except Exception as e:
            log.error(f"Error preprocessing backtest data: {e}", exc_info=True)
            return  # Exit early if preprocessing fails

        try:
            backtest_report = await mediator.send(PerformBacktestCmd())
            log.info(f"\n\nBacktest result:\n\n{backtest_report}")
        except Exception as e:
            log.error(f"Error performing backtest: {e}", exc_info=True)

    except Exception as e:
        log.critical(f"Unhandled exception in main: {e}", exc_info=True)
        raise  # Optionally re-raise if you want to crash


if __name__ == "__main__":
    log.info("--- START ---")
    try:
        asyncio.run(main())
    except Exception as e:
        log.critical(f"Fatal error running main: {e}", exc_info=True)
    log.info("--- END ---")
