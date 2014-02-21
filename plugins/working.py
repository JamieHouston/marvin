from util import hook,storage

@hook.regex(r'(working on )(?P<task>[\w\d\s]*)', run_always=True)
def working_on(bot_input, bot_output):
    "working on [task] -- lets me know you're working on that task"

    if bot_input.groupdict():
        task = bot_input.groupdict()["task"]
        nick = bot_input.nick
        storage.set_value("workingon:{0}".format(nick), task)
        bot_output.say("Got it.  {0} is working on {1}.  At least that's what I should tell the boss...".format(nick, task))

@hook.regex(r'(what is )(?P<nick>[\w\d]*) (working on)', run_always=True)
def working_list(bot_input, bot_output):
    "what is [nick] working on (or doing or whatever) -- lets you know what (nick) pretends he's working on"
    if bot_input.groupdict():
        nick = bot_input.groupdict()["nick"]
        task = storage.get_value("workingon:{0}".format(nick))
        bot_output.say("Supposedly {0} is working on {1}".format(nick, task))