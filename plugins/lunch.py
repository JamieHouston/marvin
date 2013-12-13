from util import hook, web

@hook.command
def lunch(bot_input, bot_output):
    rests = web.get_json("http://lunchpad.meteor.com/restaurants/trending")

    for rest in rests:
    	bot_output.say(rest["name"])
    	for user in rest["users"]:
    		bot_output.say("  " + user["email"])
    	bot_output.say()

# @hook.regex(r'where is (?P<user>.*) for lunch')
# def eat_lunch(bot_input, bot_output):
