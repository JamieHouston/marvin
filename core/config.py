import inspect
import json
import os


def save(conf):
    json.dump(conf, open('config', 'w'), sort_keys=True, indent=2)

if not os.path.exists('config'):
    open('config', 'w').write(inspect.cleandoc(
        r'''
        {
          "connections":
          {
            "bot":
            {
              "flow_user_api_key": "API_KEY",
              "flow_token": "FLOW_TOKEN",
              "nick": "Marvin",
              "channel": "daptiv/bot",
              "debug": "False",
              "username": "USERNAME",
              "password": "PASSWORD",
              "master": "NICKNAME",
              "chattiness": 0.01
            },
            "console":
            {
              "nick": "Marvin",
              "debug": "False",
              "master": "NICKNAME",
            }
          },
          "enabled_plugins": [],
          "disabled_plugins": [],
          "disabled_commands": [],
          "redis_connection": {
            "server": "localhost",
            "port": : 6379
          },
          "acls": {},
          "api_keys": {},
          "credentials":{
            "github":{
                "login": "USERNAME",
                "password": "PASSWORD"
            },
            "target_process":{
                "login": "USERNAME",
                "password": "PASSWORD",
                "url": "http://daptiv.tpondemand.com/api/v1/",
                "team_name": "HRV"
            },
            "teamcity":{
                login: "USERNAME",
                "password": "PASSWORD",
                "server": "teamcity"
            }
          },
          "censored_strings":
          [
            "DCC SEND",
            "1nj3ct",
            "thewrestlinggame",
            "startkeylogger",
            "hybux",
            "\\0",
            "\\x01",
            "!coz",
            "!tell /x"
          ]
        }''') + '\n')


def config():
    # reload config from file if file has changed
    config_mtime = os.stat('config').st_mtime
    if bot._config_mtime != config_mtime:
        try:
            bot.config = json.load(open('config'))
            bot._config_mtime = config_mtime
        except ValueError, e:
            print 'ERROR: malformed config!', e


bot._config_mtime = 0
