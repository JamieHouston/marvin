from flowdock import JSONStream, Chat
from core import marvin
from util import logger
from modules import markov

class Blob:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class FlowBot():

    def __init__(self, config):
        self.setup(config)

    def setup(self, config):
        self.FLOW_USER_API_KEY = config["flow_user_api_key"]
        self.FLOW_TOKEN = config["flow_token"]
        self.FLOW_CHANNELS = config["channels"]
        self.debug = config["debug"]
        self.nick = config["nick"]

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
                input_command = data["content"].lower()
                marvin.input(input_command, bot, self)



    def run(self):
        #marvin.say_hi(self)
        self.parse_stream()
