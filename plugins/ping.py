from util import hook
import random
import socket

@hook.command
def ping(bot_input, bot_output):
    """.ping -- see if I'm actually listening or off in the corner sleeping"""
    bot_output.say(random.choice(bot_output.responses["pinging"]))


@hook.command
def location(bot_input, bot_output):
    """.location -- get my ip address and hostname"""
    hostname = socket.gethostname()
    ip = socket.gethostbyname(socket.gethostname())
    bot_output.say("{0} - {1}".format(hostname, ip))
