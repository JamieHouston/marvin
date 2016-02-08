from util import web, hook
import random

@hook.command
@hook.regex(r'yo.*(mom|mama)')
def mamma(bot_input, bot_output):
    url = 'https://raw.githubusercontent.com/rdegges/yomomma-api/master/jokes.txt'
    responses = web.get_text(url)
    if responses and len(responses):
        lines = responses.split('\n')
        line = random.choice(lines)
        bot_output.say(line)