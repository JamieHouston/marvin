from util import storage, hook
import random

list_name = "game:crazyphrases:users"
phrases = ("I can't wait until Monday", "That's very true.", "I can't believe I just thought that.")

@hook.regex(r'play crazy phrases')
def crazy_phrases(bot_input, bot_output):
    phrase = random.choice(phrases)
    storage.set_hash_value(list_name, bot_input.nick, phrase)
    bot_output.say("you're in {0}".format(bot_input.nick))
    user = bot_output.get_user_by_name(bot_input.nick)
    bot_output.private_message(str(user["id"]), "Your phrase is: %s" % phrase)

@hook.regex(r'crazy phrases users')
def crazy_phrases_users(bot_input, bot_output):
    users = storage.get_random_value(list_name)
    bot_output.say("Current Users Playing: ")
    bot_output.say(", ".join(users))
