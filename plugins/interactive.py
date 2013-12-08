from util import hook
import random

@hook.regex(r'(?i)thank(s| you)')
def thanks(input, output):
    welcome = ("You're welcome, {0}", "For what {0}?", "No problem, {0}", "Why {0}?", "Okay, {0}",
        "Why bother, {0}.")
    output.say(random.choice(welcome).format(input["nick"]))
