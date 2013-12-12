#!/usr/bin/env python
__author__ = 'Steve Hayes'

import os
import random
import json
from util import hook

l = list()

@hook.command
def personality(bot_input, bot_output):
    quote_to_say = random.sample(l, 1)[0]
    bot_output.say(quote_to_say)


@hook.regex(r'change personality (?P<name>[\w\d\s]*)')
def get_personality(bot_input, bot_output):
    if bot_input.groupdict():
        personality_name = bot_input.groupdict()["name"]
        if personality_name:
            bot_personality = load_personality(personality_name)
            messages = json.loads(bot_personality)
            if bot_personality:
                bot_output.say("Personality Override. Loading " + bot_personality)
            else:
                bot_output.say("It seems that test subject is no longer...available")


def load_personality(personality_name):
    new_personality = ''
    f = open('personalities/{0}.txt'.format(personality_name.lower()), 'r')
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