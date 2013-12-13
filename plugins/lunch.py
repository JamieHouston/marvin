from util import hook, web

@hook.regex(r'lunchbot add me to (?P<rest>.*)')
def add_to_lunch(bot_input, bot_output):
    username = bot_input.nick
    email = bot_output.get_user_by_name(username)["email"]
    restaurant_name = bot_input.groupdict()["rest"]

    rests = web.get_json("http://lunchpad.hq.daptiv.com:3000/restaurants")
    restId = 0
    for it in rests:
        if it["name"] == restaurant_name:
            restId = it["_id"]

    url = "http://lunchpad.hq.daptiv.com:3000/restaurant/{0}/add/{1}".format(restId,email)
    result = web.get_json(url)
    bot_output.say('added you to %s.  Enjoy your lunch, sir.' % restaurant_name)
    bot_output.say("Just kidding. I hope they poison you.")


#@hook.regex(r'lunchbot[((?! add).*$)$')
@hook.command
def lunchbot(bot_input, bot_output):
    rests = web.get_json("http://lunchpad.hq.daptiv.com:3000/restaurants/trending")
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
