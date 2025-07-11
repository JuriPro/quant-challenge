# Точка входа для реализации

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

    # Send a command
    collect_l2_result = await mediator.send(CollectL2data(symbol='BTCUSDT'))
    print(collect_l2_result)


if __name__ == "__main__":
    log.info("--- START ---")

    asyncio.run(main())

    log.info("--- END ---")
