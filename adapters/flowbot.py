from flowdock import JSONStream
from core import marvin
from util import logger, web, dictionaryutils
import random


class BotInput(object):
    def __getitem__(self, val):
        return self.__dict__[val]

    def __setitem__(self, key, value):
        self[key] = value


class BotOutput():

    def __init__(self, config):
        self.users = []
        self.user = None
        self.setup(config)
        self.spoken = False

    def setup(self, config):
        for k, v in config.items():
            setattr(self, k, v)

    def filter_words(self, msg):
        return msg

    def say(self, msg):
        if not msg or len(msg) < 1:
            return
        if hasattr(self, 'user_nick'):
            msg = self.filter_words(msg).format(self.user_nick)

        logger.log("sending message %s" % msg[:20])
        channel_pieces = self.channel.split("/")
        url = "https://api.flowdock.com/flows/%s/%s/messages" % (channel_pieces[0], channel_pieces[1])
        data = {"event": "message", "content": msg}
        web.post_json(url, self.username, self.password, **data)
        self.spoken = True

    def private_message(self, user, msg):
        logger.log("sending private message %s" % msg[:20])
        url = "https://api.flowdock.com/private/{0}/messages".format(user)
        data = {"event": "message", "content": msg}
        web.post_json(url, self.username, self.password, **data)
        self.spoken = True

    def get_users(self):
        endpoint = "users"
        url = "https://api.flowdock.com/v1/%s"

        user_endpoint = url % endpoint
        logger.log("hitting endpoint: %s" % user_endpoint)
        self.users = web.get_json(user_endpoint, self.username, self.password)
        return self.users

    def get_user_by_id(self, user_id):
        if not self.users:
            self.get_users()
        user = [u for u in self.users if str(u["id"]) == user_id]
        if user and len(user):
            return user[0]
        return "anonymous"

    def get_user_by_name(self, user_name):
        if not self.users:
            self.get_users()
        user = [u for u in self.users if u["nick"].lower() == user_name.lower()]
        if user and len(user):
            return user[0]
        return {"nick": "anonymous", "id": 0}

    def get_user_by_email(self, user_email):
        if not self.users:
            self.get_users()
        user = [u for u in self.users if str(u["email"]) == user_email]
        if user and len(user):
            return user[0]
        return {"nick": user_email}

    def _parse_stream(self, bot):
        stream = JSONStream(self.flow_user_api_key)
        gen = stream.fetch([self.channel], active=True)
        for data in gen:
            process_message = type(data) == dict and (data['event'] == "message" or data['event'] == "comment")
            if process_message and ("user" in data and self.user != data["user"]):
                self.spoken = False
                bot_input = BotInput()
                if type(data['content']) is dict:
                    bot_input.message = data["content"]['text']
                elif "content" in data:
                    bot_input.message = data["content"]
                else:
                    break
                if "user" in data and int(data["user"]) > 0:
                    try:
                        bot_input.nick = self.get_user_by_id(data["user"])["nick"]
                        self.user_id = data["user"]
                        if random.random() < (self.chattiness / 100):
                            logger.log("Randomly sending message to %s" % bot_input.nick)
                            self.private_message(data["user"], random.choice(self.responses["private_messages"]))
                    except Exception as e:
                        logger.error(e)
                        self.say(bot.responses["stranger"])
                elif "external_name" in data:
                    bot_input.nick = data["external_name"]
                else:
                    bot_input.nick = "anonymous"
                bot_input.bot = bot
                self.user_nick = bot_input.nick

                marvin.process(bot_input, self)


    def run(self, bot):
        self.user = str(self.get_user_by_name(self.nick)["id"])
        marvin.say_hi(self)
        self._parse_stream(bot)
