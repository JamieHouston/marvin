from util import hook
from gitty import Github_Helper
from target_process import Target_Process

@hook.command
def pull(bot_input, bot_output):
    ".pull [branch] -- creates a pull request."
    branch_name = bot_input.input_string.lower()

    if branch_name:
        story_number = branch_name.split('-')[0]

    gh = Github_Helper(bot_input, bot_output)
    #tp = Target_Process(bot_input.bot.credentials["target_process"]["url"], bot_input.bot.credentials["target_process"]["login"], bot_input.bot.credentials["target_process"]["password"])
    team_members = gh.get_team_members()
