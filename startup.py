import config
from adapters.flowbot import BotOutput
from util import logger


def main():
    logger.log('starting')
    bot = BotOutput(config)
    logger.log('running')
    bot.run()

if __name__ == "__main__":
    main()

