from util import hook, storage
from .github import Github
import random

@hook.command
def github(bot_input, bot_output):
    ".github [username] -- gives a list of pending pull requests for user. Ommitting username uses last one passed in"
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
    repos = org.get_repos()
    found_pull_requests = False
    bot_output.say(random.choice(bot_output.responses["github"]).format(bot_input.nick))

    for repo in repos:
        pull_requests = get_pull_requests(repo, github_name)
        if pull_requests:
            bot_output.say('\n'.join(pull_requests))
            found_pull_requests = True

    if found_pull_requests:
        bot_output.say('Think I got them all. Good luck with that.')
    else:
        bot_output.say(random.choice(bot_output.responses["nothing_for_you"]))


def get_pull_requests(repo, github_name):
    results = []
    search_string = "[ ] @{0}".format(github_name)
    open_pull_requests = repo.get_pulls("open")
    if open_pull_requests:
        for pull in open_pull_requests:
            if pull.body and search_string in pull.body:
                results.append("{0} - {1}/files?w=1".format(pull.title, pull.html_url))
    return results