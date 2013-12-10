from util import hook, web

@hook.regex(r'http')
def url_title(bot_input, bot_output):
    bot_output.say(web.get_title(bot_input.message))
