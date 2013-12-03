import config
from flowbot import FlowBot
from utils import logger


def main():
    logger.log('starting')
    bot = FlowBot(config)
    logger.log('running')
    bot.run()

if __name__ == "__main__":
    main()
