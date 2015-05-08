import random

from util import hook, logger

from chatterbot import ChatBot

chatty = ChatBot("Marvin")
talked_to = False

@hook.regex('.*', run_always=True)
def chat(bot_input, bot_output):
    global chatty
    global talked_to

    if bot_input.bot_speaking:
        return

    message = bot_input.input_string.replace(bot_output.nick.lower(), '{user_nick}')
    response = chatty.get_response(message)
    if (bot_input.direct_message or talked_to or random.randrange(10) == 1) and response:
        bot_output.say(response)
        talked_to = bot_input.direct_message
