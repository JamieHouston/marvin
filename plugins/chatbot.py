from util import hook
from chatterbot import ChatBot

chatty = ChatBot("Marvin")


@hook.regex('.*', run_always=True)
def chat(bot_input, bot_output):
    global chatty

    message = bot_input.input_string.replace(bot_output.nick.lower(), '')
    response = chatty.get_response(message)
    if response:
        bot_output.say(response)
