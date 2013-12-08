from core import marvin
from util.dictionaryutils import BotInput
class ConsoleOutput():
    def __init__(self, config):
        print "Hello"


    def say(self, msg):
        print msg


    def run(self, bot):
        nick = raw_input("What shall I call you? ")
        print "Well hello there %s.  What can I do for you?" % nick
        while True:
            message = raw_input("> ")
            if "exit" in message:
                print "Well that's rude.  Goodbye"
                exit()
            input = BotInput({
                    "message": message,
                    "nick": nick
                })
            marvin.process(input, self, bot)

