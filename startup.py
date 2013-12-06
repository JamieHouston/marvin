import config
from core.flowbot import FlowBot
from util import logger


def main():
    logger.log('starting')
    bot = FlowBot(config)
    logger.log('running')
    bot.run()

if __name__ == "__main__":
    main()

