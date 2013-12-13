from util import hook, web

@hook.command
def lunch(bot_input, bot_output):
    bot_output.say("lunch time")

@hook.regex(r'lunch for (*.)')
def eat_lunch(bot_input, bot_output):
    bot_output.say("lunch time")
