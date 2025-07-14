# Точка входа для реализации

from CONFIG import cfg

# CQRS support
from application.handlers import *
from application.mediator import Mediator

# Add logger
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
    mediator = Mediator()

    # Register handlers
    mediator.register_command_handler(CollectL2data, CollectL2DataHandler())
    mediator.register_command_handler(PreprocessRawL2Data, PreprocessBacktestData())
    mediator.register_command_handler(PerformBacktestCmd, PerformBacktest())

    # Send a command
    if not cfg['use_previous_data']:
        collect_l2_result = await mediator.send(
            CollectL2data(symbol=cfg['symbol'],
                          depth=cfg['depth'],
                          collection_time_min=cfg['collection_time_min'],
                          collection_interval_sec=cfg['collection_interval_sec']))
        log.info(collect_l2_result)

    backtest_data_fpath = await mediator.send(PreprocessRawL2Data())
    log.info(backtest_data_fpath)

    backtest_report = await mediator.send(PerformBacktestCmd())
    log.info(f"\n\nBacktest result:\n\n{backtest_report}")


if __name__ == "__main__":
    log.info("--- START ---")
    asyncio.run(main())
    log.info("--- END ---")
