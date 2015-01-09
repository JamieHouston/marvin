from util import hook
import github
import random

@hook.command
def pull(bot_input, bot_output):
    ".pull [team_name] -- creates a pull request."

    if bot_input.input_string:
        team_name = bot_input.input_string.lower()