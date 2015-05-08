from util import hook, logger
from chatterbot import ChatBot

chatty = ChatBot("Marvin")


@hook.regex('.*', run_always=True)
def chat(bot_input, bot_output):
    global chatty

    message = bot_input.input_string.replace(bot_output.nick.lower(), '{user_nick}')
    response = chatty.get_response(message)
#    logger.log("direct_message:{0}. Chatbot response: {1}".format(bot_input.direct_message, response))
    if bot_input.direct_message and response:
        bot_output.say(response)
