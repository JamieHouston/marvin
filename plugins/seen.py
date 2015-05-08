from util import hook

@hook.command
def seen(bot_input, bot_output):
    bot_output.say("No, and stop asking, {user_nick}")