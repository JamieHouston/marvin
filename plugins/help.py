import re
from util import hook

@hook.command(autohelp=False)
def help(bot_input, bot_output):
    ".help [command] -- gives a list of commands or help for a command if it's included"

    bot = bot_input.bot
    funcs = {}
    #disabled = bot.config.get('disabled_plugins', [])
    #disabled_comm = bot.config.get('disabled_commands', [])
    for command, (func, args) in bot.commands.items():
        fn = re.match(r'^plugins.(.+).py$', func._filename)
        #if fn.group(1).lower() not in disabled:
            #if command not in disabled_comm:
        if func.__doc__ is not None:
            if func in funcs:
                if len(funcs[func]) < len(command):
                    funcs[func] = command
            else:
                funcs[func] = command

    commands = dict((value, key) for key, value in funcs.items())

    help_text = []

    help_text.append("You do need help.  But I supposed I can offer some insight into how to talk to something as advanced as myself.")
    help_text.append("I am the Marginally Accurate Resource for Vocalizing Immature Communication")
    help_text.append("You can ask me to run commands, ask me questions, and just talk to me.")
    help_text.append("To run a command, preface it with a period (.)")
    help_text.append("To talk to me, just include my name and if I haven't commited bot suicide recently I'll reply.  Although you may not like what I have to say...")
    help_text.append("Like the NSA, I'm always listening, so if I pick up on something someone says and I have a smart-ass response, make no mistake that I will answer it.")

    if not bot_input.input_string:
        help_text.append("For details on a particular command, include it after help.")
        help_text.append("The available commands are: %s" % ', '.join(sorted(commands)))
    else:
        if bot_input.input_string in commands:
            help_text.append(commands[bot_input.input_string].__doc__)

    bot_output.say('\n'.join(help_text))