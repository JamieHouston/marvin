from util import hook
from gitty import Github_Helper
from target_process import Target_Process

@hook.command
def pull(bot_input, bot_output):
    ".pull [options] -- creates a pull request."

    gh = Github_Helper(bot_input, bot_output)
    #tp = Target_Process(bot_input.bot.credentials["target_process"]["url"], bot_input.bot.credentials["target_process"]["login"], bot_input.bot.credentials["target_process"]["password"])

    gh.teamstatus()
    #tp.get_object("user_story")