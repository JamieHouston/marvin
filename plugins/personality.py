import random
import json
from util import hook, logger

l = list()

@hook.command
def personality(bot_input, bot_output):
    quote_to_say = random.sample(l, 1)[0]
    bot_output.say(quote_to_say)


@hook.regex(r'change personality (?P<name>[\w\d\s]*)')
def get_personality(bot_input, bot_output):
    if bot_input.groupdict():
        personality_name = bot_input.groupdict()["name"]
        if personality_name and personality_name.lower() != bot_output.nick.lower():
            try:
                bot_personality = load_personality(personality_name)
                if bot_personality:
                    bot_output.responses = bot_personality
<<<<<<< HEAD
                    bot_output.personality = personality_name
=======
                    bot_output.say("Personality Override. Loading " + personality_name)
>>>>>>> ed0007a4ea6700c7787df32eb18cdc03d1226ca5
                else:
                    bot_output.say("It seems that test subject, I mean {0} is no longer...available").format(personality_name)
            except:
                bot_output.say("nice try, asshole")
        else:
            bot_output.say("I'm schizophrenic, and so am I")


@hook.regex(r'who dat')
def get_current_personality(bot_input, bot_output):
    bot_output.say("THIS IS {0}".format(bot_output.personality))

@hook.regex(r'who is your jedi master')
def get_current_master(bot_input, bot_output):
    bot_output.say("I serve {0}".format(bot_output.master))


def load_personality(personality_name):
    new_personality = ''
    try:
        f = open('personalities/{0}.txt'.format(personality_name.lower()), 'r')
    except:
        #logger.log("Couldn't load file {0}".format(personality_name))
        f = open('personalities/default.txt'.format(personality_name.lower()), 'r')
    for line in f:
        line = line.strip()
        if line == '%':
            personality_name.append(new_personality)
            new_personality = ''
        else:
            if new_personality != '':
                new_personality += ' '
            new_personality += line
    f.close()
    return json.loads(new_personality)