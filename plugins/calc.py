#!/usr/bin/env python
# coding=utf-8
"""
calc.py - Phenny Calculator Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

from util import hook,web

@hook.command
def calculate(bot_input, bot_output):
    ".calculate <expression> - Calculates expression.  Duh."
    if not bot_input.input_string:
        bot_output.say("Nothing to calculate.")
        return

    q = bot_input.input_string.encode('utf-8')
    q = q.replace('\xcf\x95', 'phi')  # utf-8 U+03D5
    q = q.replace('\xcf\x80', 'pi')  # utf-8 U+03C0
    uri = 'http://www.google.com/ig/calculator?q='
    bytes = web.get(uri + web.urllib.quote(q))
    parts = bytes.split('",')
    answer = [p for p in parts if p.startswith('rhs: "')][0][6:]
    if answer:
        answer = answer.decode('unicode-escape')
        answer = ''.join(chr(ord(c)) for c in answer)
        answer = answer.decode('utf-8')
        answer = answer.replace(u'\xc2\xa0', ',')
        answer = answer.replace('<sup>', '^(')
        answer = answer.replace('</sup>', ')')
        answer = web.decode(answer)
        bot_output.say(answer)
    else:
        bot_output.say('Sorry, no result.')

@hook.command
def py(bot_input, bot_output):
    query = bot_input.input_string.encode('utf-8')
    uri = 'http://tumbolia.appspot.com/py/'
    answer = web.get(uri + web.urllib.quote(query))
    if answer:
        bot_output.say(answer)
    else:
        bot_output.reply('Sorry, no result.')


@hook.command
def wa(bot_input, bot_output):
    if not bot_input.input_string:
        return bot_output.say("No search term.")
    query = bot_input.input_string.encode('utf-8')
    uri = 'http://tumbolia.appspot.com/wa/'
    answer = web.get(uri + web.urllib.quote(query.replace('+', '%2B')))
    if answer:
        bot_output.say(answer)
    else:
        bot_output.reply('Sorry, no result.')
