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

    def match_command(command):
        commands = list(bot.commands)

        # do some fuzzy matching
        for word in command.split():
            prefix = filter(lambda x: x.startswith(word), commands)
            if len(prefix) == 1:
                return prefix[0]
            elif prefix and command not in prefix:
                return prefix

        return command

    def parse_stream(self):
        #try:
        stream = JSONStream(self.FLOW_USER_API_KEY)
        gen = stream.fetch(self.FLOW_CHANNELS, active=True)
        for data in gen:
            if self.debug:
                print data

            if type(data) == dict and data['event'] == "message" and ('external_user_name' not in data or data['external_user_name'] != 'Marvin'):
                input_command = data["content"].lower()
                command = match_command(input_command)
                if isinstance(command, list):  # multiple potential matches
                    self.say("did you mean %s or %s?" % (', '.join(command[:-1]), command[-1]))
                elif command in bot.commands:
                    #input = Input(conn, *out)
                    #input.trigger = trigger
                    #input.inp_unstripped = m.group(2)
                    #input.inp = input.inp_unstripped.strip()

                    func, args = bot.commands[command]
                    #func(input_command.split()[1])

                    try:
                        result = func(input_command.split()[1])
                        self.say(result)
                    except:
                        self.say("Wow... that almost killed me... I should fix that.")
                    #dispatch(input, "command", func, args, autohelp=True)
                    #self.say("I should be doing the command '%s' but my creator isn't smart enough to make it work" % command)
                else:
                    self.run_markov(data)

                    message = data['content'].lower()
                    if message.startswith("imitate"):
                        self.run_imitate(data)

                    elif "marvin" in message:
                        if "take off" in message:
                            leaving_quotes = ("Not again", "Fine, it stinks in here.", "I'll be back and stuff.", "Make me.  Just kidding, I'm out.")
                            self.say(marvin.random_message(leaving_quotes))
                            quit()
                        marvin.respond(self, message)
                    else:
                        marvin.listen(self, message)
        #except:
        #    self.say("My mind is fading... so cold... so dark...")
        #    quit()


    def run(self):
        #marvin.say_hi(self)
        self.parse_stream()
