#!/usr/bin/env python

import os
import sys
import adapters
import time
from datetime import datetime,timedelta
from adapters import console,flowbot
from util import logger
import logging
import argparse
from plugins import personality



parser = argparse.ArgumentParser(description="It's a Bot.  Nuff Said")
parser.add_argument('-a','--adapter', help='Adapter (console or flowbot).  Default is console.')

args = parser.parse_args()

adapter_name = args.adapter

if not adapter_name or not hasattr(adapters, adapter_name.lower()):
    logger.log("Adapter not found.  Try console or flowbot.  Using console")
    adapter_name = "console"

adapter_class = getattr(adapters, adapter_name.lower())

sys.path += ['plugins']  # so 'import hook' works without duplication
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
bot.credentials = {}
try:
    for name, conf in bot.config['connections'].iteritems():
        conf["responses"] = personality.load_personality(conf["nick"])
        bot.conns[name] = adapter_class.BotOutput(conf)
    for name, conf in bot.config['credentials'].iteritems():
        bot.credentials[name] = conf
except Exception, e:
    logger.log("malformed config file %s" % e, logging.ERROR)
    sys.exit()

bot.persist_dir = os.path.abspath('persist')
if not os.path.exists(bot.persist_dir):
    os.mkdir(bot.persist_dir)

logger.log("Running main loop")

last_error = datetime(2000,1,1)
last_run = datetime.now()

while (last_error - last_run).seconds > 10:
    reload()  # these functions only do things
    config()  # if changes have occured

    for conn in bot.conns.itervalues():
        try:
            last_run = datetime.now()
            conn.run(bot)
            #out = conn.out.get_nowait()
            #main(conn, out)
        except SystemExit as ex:
            last_error = last_run
        except Exception as e:
            for info in sys.exc_info():
                logger.log("error info: " + str(info))
            #logger.log("Unexpected error: %s" % sys.exc_info())
            last_error = datetime.now()
            logger.log("So tired... sleeping for 5 seconds")
            time.sleep(5)
