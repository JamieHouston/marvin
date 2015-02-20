from util import hook
import random

@hook.command
def ping(bot_input, bot_output):
    bot_output.say(random.choice(bot_output.responses["pinging"]))
