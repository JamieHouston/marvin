from core import marvin
from util.dictionaryutils import Blob

class BotInput(object):
    def __getitem__(self, val):
        return self.__dict__[val]

    def __setitem__(self, key, value):
        self[key] = value

class BotOutput():
    def __init__(self, config):
        print "Hello"


    def say(self, msg):
        print msg


    def run(self, bot):
        self.nick = raw_input("What shall I call you? ")
        print("Well hello there {}.  What can I do for you?".format(self.nick))
        while True:
            message = raw_input("> ")
            if "exit" in message:
                print("Well that's rude.  Goodbye")
                exit()
            bot_input = BotInput()
            bot_input.message = message
            bot_input.nick =self.nick
            bot_input.bot = bot
            marvin.process(bot_input, self)

