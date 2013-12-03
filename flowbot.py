from flowdock import JSONStream, Chat
from utils import logger
from modules import markov
import marvin

class Blob:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class FlowBot():

    def __init__(self, config):
        self.setup(config)

    def setup(self, config):
        self.FLOW_USER_API_KEY = config.flow_user_api_key
        self.FLOW_TOKEN = config.flow_token
        self.FLOW_CHANNELS = config.flow_channels
        self.debug = config.debug
        self.nick = config.nickname

        self.chat = Chat(self.FLOW_TOKEN)

    def say(self, msg):
        logger.log("sending message %s" % msg)
        self.chat.post(msg, 'Marvin')


    def run_markov(self, data):
        markov_input = Blob(**data)
        markov_input.nick = data['user']
        markov.markov_master(self, markov_input)

    def run_imitate(self, data):
        markov_input = Blob(**data)
        markov_input.nick = data['user']
        markov.markov_imitate(self, markov_input)

    def parse_stream(self):
        #try:
        stream = JSONStream(self.FLOW_USER_API_KEY)
        gen = stream.fetch(self.FLOW_CHANNELS, active=True)
        for data in gen:
            if self.debug:
                    print data

            if type(data) == dict and data['event'] == "message" and ('external_user_name' not in data or data['external_user_name'] != 'Marvin'):
                self.run_markov(data)

                message = data['content'].lower()
                if message.startswith("imitate"):
                    self.run_imitate(data)

                elif message.startswith("marvin"):
                    if "take off" in message:
                        self.say("Later losers.")
                        quit()
                    marvin.respond(self, message)
                else:
                    marvin.listen(self, message)
        #except:
        #    self.say("My mind is fading... so cold... so dark...")
        #    quit()


    def run(self):
        marvin.say_hi(self)
        self.parse_stream()
