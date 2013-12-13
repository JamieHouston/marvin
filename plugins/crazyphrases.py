from util import storage, hook

list_name = "game:crazyphrases:users"
list_name = "game:crazyphrases:users"
@hook.regex(r'play crazy phrases')
def crazy_phrases(bot_input, bot_output):
    storage.set_hash_value(list_name, bot_input.nick, 0)
    bot_output.say("you're in {0}".format(bot_input.nick))

@hook.regex(r'crazy phrases users')
def crazy_phrases_users(bot_input, bot_output):
    users = storage.g(list_name)
    bot_output.say("Current Users Playing: ")
    bot_output.say(", ".join(users))
