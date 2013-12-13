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
        self.setup(config)

    def setup(self, config):
        self.flow_user_api_key = config["flow_user_api_key"]
        # chattiness on a scale of 0 to 1 (most is every time)
        self.chattiness = 0.01
        self.flow_token = config["flow_token"]
        self.channels = config["channels"]
        self.debug = bool(config["debug"])
        self.nick = config["nick"]
        self.username = config["username"]
        self.password = config["password"]
        self.master = config["master"]
        self.users = []
        self.responses = config["responses"]

    # def filter_words(self, msg):
    #     return msg.replace("s","th")


    def say(self, msg):
        #msg = self.filter_words(msg)
        logger.log("sending message %s" % msg[:20])
        url = "https://api.flowdock.com/flows/{0}/{1}/messages".format("daptiv", "hackday")
        data = {"event": "message", "content": msg}
        response = web.post_json(url, self.username, self.password, **data)

    def private_message(self, user, msg):
        logger.log("sending private message %s" % msg[:20])
        url = "https://api.flowdock.com/private/{0}/messages".format(user)
        data = {"event": "message", "content": msg}
        response = web.post_json(url, self.username, self.password, **data)


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
        user = [u for u in self.users if str(u["nick"]) == user_name]
        if user and len(user):
            return user[0]
        return "anonymous"


    def get_user_by_email(self, user_email):
        if not self.users:
            self.get_users()
        user = [u for u in self.users if str(u["email"]) == user_email]
        if user and len(user):
            return user[0]
        return {"nick": user_email}

    def _parse_stream(self, bot):
        stream = JSONStream(self.flow_user_api_key)
        gen = stream.fetch(self.channels, active=True)
        for data in gen:
            process_message = type(data) == dict and (data['event'] == "message" or data['event'] == "comment")
            if process_message and ("user" in data and self.user != data["user"]):
                bot_input = BotInput()
                if type(data['content']) is dict:
                    bot_input.message = data["content"]['text'].lower()
                elif "content" in data:
                    bot_input.message = data["content"].lower()
                else:
                    break
                if ("user" in data and int(data["user"]) > 0):
                    if (random.random() < self.chattiness):
                        self.private_message(data["user"], random.choice(self.responses["private_messages"]))
                    bot_input.nick = self.get_user_by_id(data["user"])["nick"]
                elif ("external_name" in data):
                    bot_input.nick = data["external_name"]
                else:
                    bot_input.nick = "anonymous"
                bot_input.bot = bot

                marvin.process(bot_input, self)


    def run(self, bot):
        self.user = str(self.get_user_by_name(self.nick)["id"])
        marvin.say_hi(self)
        self._parse_stream(bot)
