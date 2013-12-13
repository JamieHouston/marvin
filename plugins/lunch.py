from util import hook, web

@hook.command
def lunch(bot_input, bot_output):
    rests = web.get_json("http://lunchpad.meteor.com/restaurants/trending")
    to_say = []

    for rest in rests:
        to_say.append(rest["name"])
        for user in rest["users"]:
            flowuser = bot_output.get_user_by_email(user)["nick"]
            to_say.append("- " + flowuser)

    joined = '\n'.join(to_say)
    bot_output.say(joined)

# @hook.regex(r'where is (?P<user>.*) for lunch')
# def eat_lunch(bot_input, bot_output):
