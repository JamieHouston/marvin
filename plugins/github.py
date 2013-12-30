from util import hook, storage
from github import Github

@hook.command
def github(bot_input, bot_output):
    ".github [username] -- gives a list of pending pull requests for user. Ommitting username uses last one passed in"
    found_requests = False
    if bot_input.input_string:
        github_name = bot_input.input_string
        storage.set_value("github:%s" % bot_output.nick, github_name)
    else:
        github_name = storage.get_value("github:%s" % bot_output.nick)

    if github_name:
        gi = Github(bot_input.credentials["login"], bot_input.credentials["password"])
        org = gi.get_organization("daptiv")
        repo = org.get_repo("ppm")
        search_string = "[ ] @{0}".format(github_name)
        open_pull_requests = repo.get_pulls("open")
        if open_pull_requests:
            for pull in open_pull_requests:
                if search_string in pull.body:
                    found_requests = True
                    bot_output.say("%s - %s" % (pull.title, pull.html_url))
        if not found_requests:
            bot_output.say("How weak... nothing for you...")