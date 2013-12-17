from util import hook, web

@hook.command
def joke(bot_input, bot_output):
    story = web.get_json("http://webknox.com/api/jokes/random?apiKey=bdihdcabiccdmcxpkltuvoeyaqbzcgx")
    bot_output.say(story)