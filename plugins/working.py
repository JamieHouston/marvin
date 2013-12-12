# from util import hook,storage
#
# @hook.regex(r'(working on )(?P<task>[\w\d\s]*)')
# def working_on(bot_input, bot_output):
#     if bot_input.groupdict():
#         task = bot_input.groupdict()["task"]
#         nick = bot_input.nick
#         storage.set_value("workingon:{0}".format(nick), task)
#         bot_output.say("Got it.  {0} is working on {1}.  At least that's what I should tell the boss...".format(nick, task))
#
# @hook.regex(r'(what is (?P<nick>[\w\d]*)')
# def working_list(bot_input, bot_output):
#     if bot_input.groupdict():
#         nick = bot_input.groupdict()["nick"]
#         task = storage.get_value("workingon:{0}".format(nick))
#         bot_output.say("Supposedly {0} is working on {1}".format(nick, task))