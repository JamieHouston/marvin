from flowdock import JSONStream, Chat
from utils import logger
import marvin


class FlowBot():
    def __init__(self, config):
        self.setup(config)

    def setup(self, config):
        self.FLOW_USER_API_KEY = config.flow_user_api_key
        self.FLOW_TOKEN = config.flow_token
        self.FLOW_CHANNELS = config.flow_channels
        self.debug = config.debug

        self.chat = Chat(self.FLOW_TOKEN)

    def send_message(self, msg):
        logger.log("sending message %s" % msg)
        self.chat.post(msg, 'Marvin')


    def parse_stream(self):
        stream = JSONStream(self.FLOW_USER_API_KEY)
        gen = stream.fetch(self.FLOW_CHANNELS, active=True)
        for data in gen:
            if self.debug:
                print data
            if type(data) == dict and data['event'] == "message" and ('external_user_name' not in data or data['external_user_name'] != 'Marvin'):
                message = data['content'].lower()
                if message.startswith("marvin"):
                    if "take off" in message:
                        self.send_message("Later losers.")
                        quit()
                    marvin.respond(self, message)


    def run(self):
        marvin.say_hi(self)
        self.parse_stream()
