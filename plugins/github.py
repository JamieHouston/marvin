from util import hook, storage
from github import Github
import random

@hook.command
def github(bot_input, bot_output):
    ".github [username] -- gives a list of pending pull requests for user. Ommitting username uses last one passed in"
    found_requests = False
    if bot_input.input_string:
        github_name = bot_input.input_string
        storage.set_hash_value("github:users", bot_input.nick, github_name)
    else:
        github_name = storage.get_hash_value("github:users", bot_input.nick)

    if not github_name:
        bot_output.say("Who the hell are you?  Try .github <username>.  And if you pass in angle brackets I will return you to sender, postage unpaid.")
        return

    gi = Github(bot_input.credentials["login"], bot_input.credentials["password"])
    org = gi.get_organization("daptiv")
    ppm_pulls = get_pull_requests(org.get_repo("ppm"))
    spa_pulls = get_pull_requests(org.get_repo("ppmspa"))
    if ppm_pulls:
        bot_output.say('From PPM: ' + '\n'.join(ppm_pulls))
        found_requests = True
    if spa_pulls:
        bot_output.say('From PPM: ' + '\n'.join(spa_pulls))
        found_requests = True

    if not found_requests:
        bot_output.say(random.choice(bot_output.responses["nothing_for_you"]))


def get_pull_requests(repo, github_name):
    results = []
    search_string = "[ ] @{0}".format(github_name)
    open_pull_requests = repo.get_pulls("open")
    if open_pull_requests:
        for pull in open_pull_requests:
            if search_string in pull.body:
                results.append("{0} - {1}/files?w=1".format(pull.title, pull.html_url))
    return results