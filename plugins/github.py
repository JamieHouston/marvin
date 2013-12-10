from util import hook
from github import Github

@hook.regex(r'(github )(?P<name>[\w\d\s]*)')
def github(bot_input, bot_output):
    if bot_input.groupdict():
        github_name = bot_input.groupdict()["name"]

        gi = Github(bot_input.credentials["login"], bot_input.credentials["password"])
        org = gi.get_organization("daptiv")
        repo = org.get_repo("ppm")
        search_string = "[ ] @{0}".format(github_name)
        for pull in repo.get_pulls("open"):
            if search_string in pull.body:
                bot_output.say("%s - %s" % (pull.title, pull.html_url))