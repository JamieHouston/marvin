#!/usr/bin/env python

import os
import Queue
import sys
import time
from adapters import console, flowbot
from util import logger
import logging

sys.path += ['plugins']  # so 'import hook' works without duplication
sys.path += ['lib']
os.chdir(sys.path[0] or '.')  # do stuff relative to the install directory


class Bot(object):
    pass


bot = Bot()

print 'Loading plugins'

# bootstrap the reloader
eval(compile(open(os.path.join('core', 'reload.py'), 'U').read(),
    os.path.join('core', 'reload.py'), 'exec'))

reload(init=True)

config()
if not hasattr(bot, 'config'):
    logger.log("no config found for bot", logging.ERROR)
    exit()

logger.log("Connecting to IRC")

bot.conns = {}

try:
    for name, conf in bot.config['connections'].iteritems():
        #bot.conns[name] = BotOutput(conf)
        bot.conns[name] = console.ConsoleOutput(conf)
        #if conf.get('ssl'):
        #    bot.conns[name] = SSLIRC(conf['server'], conf['nick'], conf=conf,
        #            port=conf.get('port', 6667), channels=conf['channels'],
        #            ignore_certificate_errors=conf.get('ignore_cert', True))
        #else:
        #    bot.conns[name] = IRC(conf['server'], conf['nick'], conf=conf,
        #            port=conf.get('port', 6667), channels=conf['channels'])
except Exception, e:
    logger.log("malformed config file %s" % e, logging.ERROR)
    sys.exit()

bot.persist_dir = os.path.abspath('persist')
if not os.path.exists(bot.persist_dir):
    os.mkdir(bot.persist_dir)

logger.log("Running main loop")

while True:
    reload()  # these functions only do things
    config()  # if changes have occured

    for conn in bot.conns.itervalues():
        try:
            conn.run(bot)
            #out = conn.out.get_nowait()
            #main(conn, out)
        except Queue.Empty:
            pass
        except Exception as e:
            logger.log("boo: %s" % e)
