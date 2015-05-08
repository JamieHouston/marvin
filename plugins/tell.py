from util import hook

@hook.regex(r'tell (?P<username>@\w+) (?P<message>.+)$', run_always=True)
def tell_him(bot_input, bot_output):
    bot_input.inp['message'] = bot_input.inp['message'].replace('I', 'They')
    bot_input.inp['message'] = bot_input.inp['message'].replace('am', 'are')
    bot_output.say("I'll tell %(username)s {user_nick} said '%(message)s\'" % bot_input.inp)