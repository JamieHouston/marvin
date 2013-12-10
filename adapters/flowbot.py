from flowdock import JSONStream, Chat
from core import marvin
from util import logger, web, dictionaryutils
from modules import markov

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
        self.flow_token = config["flow_token"]
        self.channels = config["channels"]
        self.debug = bool(config["debug"])
        self.nick = config["nick"]
        self.username = config["username"]
        self.password = config["password"]
        self.users = []

        self.chat = Chat(self.flow_token)

    def say(self, msg):
        logger.log("sending message %s" % msg)
        self.chat.post(msg, self.nick)

    def private_message(self, msg):
        logger.log("sending private message %s" % msg)
        self.chat.post(msg, self.nick)


    def get_users(self):
        endpoint = "users"
        url = "https://api.flowdock.com/v1/%s"

        user_endpoint = url % endpoint
        logger.log("hitting endpoint: %s" % user_endpoint)
        self.users = web.get_json(user_endpoint, self.username, self.password)
        return self.users


    def get_user(self, user_id):
        if not self.users:
            self.get_users()
        user = [u for u in self.users if str(u["id"]) == user_id]
        return user[0]


    def run_markov(self, data):
        markov_input = dictionaryutils.DictToObject(**data)
        user_id = data['nick']
        markov_input.nick = self.get_user(user_id)
        markov.markov_master(self, markov_input)

    def run_imitate(self, data):
        markov_input = dictionaryutils.DictToObject(**data)
        user_id = data['nick']
        markov_input.nick = self.get_user(user_id)
        markov.markov_imitate(self, markov_input)

    def _parse_stream(self, bot):
        stream = JSONStream(self.flow_user_api_key)
        gen = stream.fetch(self.channels, active=True)
        for data in gen:
            if type(data) == dict and data['event'] == "message" and ('external_user_name' not in data or data['external_user_name'] != 'Marvin'):
                bot_input = BotInput()
                bot_input.message = data["content"].lower()
                bot_input.nick =self.get_user(data["user"])["nick"]
                bot_input.bot = bot

                marvin.process(bot_input, self, bot)


    def run(self, bot):
        marvin.say_hi(self)
        self._parse_stream(bot)
