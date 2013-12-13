from util import storage, hook

@hook.regex(r'play crazy phrases')
def crazy_phrases(bot_input, bot_output):
    storage.add_to_list("game:crazyphrases:users", bot_input.nick)
    bot_output.say("you're in {0}".format(bot_input.nick))