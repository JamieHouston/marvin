#!/usr/bin/env python

import os
import random
from util import hook

l = list()


#def quote_me(phenny, input):
#    quote_to_say =random.sample(l, 1)[0]
#    return quote_to_say
#    #phenny.say(quote_to_say)

@hook.regex("quote (?P<name>\w*)")
def random_quote():
    quote_to_say =random.sample(l, 1)[0]
    return quote_to_say


def load_quotes(quote_list, file):
    new_quote = ''
    f = open(file, 'r')
    for line in f:
        line = line.strip()
        if line == '%':
            quote_list.append(new_quote)
            new_quote = ''
        else:
            if new_quote != '':
                new_quote += ' '
            new_quote += line
    f.close()

#quote_me.commands = ['quote']
#quote_me.example = '.quote'

# Load all fortunes into memory.
files = os.listdir('quotes')
for file in files:
    load_quotes(l, 'quotes/' + file)
