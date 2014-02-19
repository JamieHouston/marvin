from util import hook, web
import random

@hook.regex(r'http', run_always=True)
def url_title(bot_input, bot_output):
    try:
        if bot_input.message.endswith("gif"):
            gif(bot_input, bot_output)
        else:
            bot_output.say(web.get_title(bot_input.message))
    except:
        pass

@hook.regex('gif')
def gif(bot_input, bot_output):
    more_picture_messages = [
        "Not another picture",
        "Saw that one already",
        "Worst. Picture. Ever",
        "That the best picture you can get?",
        "That picture reminds me of your mom.",
        "If ever there was a dumber picture, I haven't seen it.",
        "Of course you'd show that picture.",
        "That's a trippy picture",
        "Is that your mom in that picture?"
    ]
    bot_output.say(random.choice(more_picture_messages))