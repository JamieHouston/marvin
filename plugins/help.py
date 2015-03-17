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

    if not bot_input.input_string:
        help_text.append("For details on a particular command, include it after help.")
        help_text.append("The available commands are: %s" % ', '.join(sorted(commands)))
    else:
        if bot_input.input_string in commands:
            help_text.append(commands[bot_input.input_string].__doc__)

    bot_output.say('\n'.join(help_text))