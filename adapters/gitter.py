from core. streaming_api import JSONStream
from core import marvin
from util import logger, web

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
        self.api_root = "https://api.gitter.im/v1/"
        self.spoken = False

    def setup(self, config):
        for k,v in config.items():
            setattr(self, k, v)

    def filter_words(self, msg):
        return msg

    def say(self, msg):
        if not msg or len(msg) < 1:
            return
        if hasattr(self, 'user_nick'):
            msg = msg.format(user_nick='@' + self.user_nick)
        logger.log("sending message %s" % msg[:20])
        url = "%srooms/%s/chatMessages" % (self.api_root, self.room_id)
        data = {"text": msg}
        web.post_json_secure(url, self.token, data)
        self.spoken = True

    def private_message(self, user, msg):
        logger.log("sending private message %s" % msg[:20])
        # TODO: Private message (listen and send)
        url = "%srooms/%s/chatMessages" % (self.api_root, self.room_id)
        data = {"event": "message", "content": msg}
        web.post_json(url, self.username, self.password, **data)

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
        rooms_endpoint = "%srooms" % self.api_root
        return web.get_json_secure(rooms_endpoint, self.token)

    def get_user_by_email(self, user_email):
        if not self.users:
            self.get_users()
        user = [u for u in self.users if str(u["email"]) == user_email]
        if user and len(user):
            return user[0]
        return {"nick": user_email}

    # TODO: I believe bot is self... need to be clearer about what is in bot_input and output
    def _parse_stream(self, bot):
        stream = JSONStream(self.token, self.room_id)
        gen = stream.fetch()
        for data in gen:
            process_message = type(data) == dict and ("text" in data)
            if process_message and ("fromUser" in data):
                from_user = data["fromUser"]["username"]
                self.spoken = False
                bot_input = BotInput()
                bot_input.message = data["text"]
                try:
                    bot_input.nick = from_user
                    #bot_input.bot_speaking = from_user.lower().startswith(self.nick.lower())
                    if from_user.lower().startswith(self.nick.lower()):
                        continue
                    self.user_id = data["fromUser"]["id"]
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
