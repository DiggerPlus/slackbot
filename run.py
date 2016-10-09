# -*- coding: utf-8 -*-

import logging
import sys
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

from slackbot.bot import Bot


def main():
    bot = Bot()
    bot.run()


if __name__ == '__main__':
    main()
