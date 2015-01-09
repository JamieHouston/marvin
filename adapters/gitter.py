from core. streaming_api import JSONStream
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
        for k,v in config.iteritems():
            setattr(self, k, v)

        self.users = []
        self.api_root = "https://api.gitter.im/v1/"

    def filter_words(self, msg):
        #filtered = web.get_text('http://www.purgomalum.com/service/plain?text={0}'.format(msg))
        #return filtered
        return msg

    def say(self, msg):
        if not msg or len(msg) < 1:
            return
        if hasattr(self, 'user_nick'):
            msg = self.filter_words(msg).format(self.user_nick)
        logger.log("sending message %s" % msg[:20])
        url = "%srooms/%s/chatMessages" % (self.api_root, self.room_id)
        data = {"text": msg}
        response = web.post_json_secure(url, self.token, data)
        self.spoken = True

    def private_message(self, user, msg):
        logger.log("sending private message %s" % msg[:20])
        # TODO: Private message (listen and send)
        #url = "https://api.flowdock.com/private/{0}/messages".format(user)
        url = "%srooms/%s/chatMessages" % (self.api_root, self.room_id)
        data = {"event": "message", "content": msg}
        response = web.post_json(url, self.username, self.password, **data)

    def get_users(self):
        user_endpoint = "%srooms/%s/users" % (self.api_root, self.room_id)
        logger.log("hitting endpoint: %s" % user_endpoint)
        self.users = web.get_json_secure(user_endpoint, self.token)
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
        user = [u for u in self.users if u["username"].lower() == user_name.lower()]
        if user and len(user):
            return user[0]
        return {"nick": "anonymous", "id": 0}

    def get_rooms(self):
        rooms_endpoint = "%srooms" % (self.api_root)
        return web.get_json_secure(rooms_endpoint, self.token)

    def get_user_by_email(self, user_email):
        if not self.users:
            self.get_users()
        user = [u for u in self.users if str(u["email"]) == user_email]
        if user and len(user):
            return user[0]
        return {"nick": user_email}

    def _parse_stream(self, bot):
        stream = JSONStream(self.token, self.room_id)
        gen = stream.fetch()
        for data in gen:
            process_message = type(data) == dict and ("text" in data)
            if process_message and ("fromUser" in data and self.nick != data["fromUser"]["username"]):
                from_user = data["fromUser"]["username"]
                self.spoken = False
                bot_input = BotInput()
                bot_input.message = data["text"]
                try:
                    bot_input.nick = from_user
                    bot_input.displayName = data["fromUser"]["displayName"]
                    self.user_id = data["fromUser"]["id"]
                    if random.random() < (self.chattiness / 100):
                        logger.log("Randomly sending message to %s" % bot_input.nick)
                        #self.private_message(data["user"], random.choice(self.responses["private_messages"]))
                except Exception as e:
                    logger.error(e)
                    self.say(bot.responses["stranger"])
                bot_input.bot = bot
                self.user_nick = bot_input.nick

                marvin.process(bot_input, self)


    def run(self, bot):
        self.user = str(self.get_user_by_name(self.nick)["id"])
        marvin.say_hi(self)
        self._parse_stream(bot)
