import json
import os

def config(bot):
    # reload config from file if file has changed
    config_mtime = os.stat('config').st_mtime
    if bot._config_mtime != config_mtime:
        try:
            bot.config = json.load(open('config'))
            bot._config_mtime = config_mtime
        except ValueError as e:
            print('ERROR: malformed config!', e)


bot._config_mtime = 0
