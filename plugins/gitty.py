from util import hook, storage
from github import Github
import random
import re
import inspect


@hook.command
def github(bot_input, bot_output):
    ".github [username] -- gives a list of pending pull requests for user. Ommitting username uses last one passed in\n.github teamstatus -- gives a list of pending pull requests for user. Ommitting teamnames uses last one passed in"
    input_argument = bot_input.input_string

    gh = Github_Helper(bot_input, bot_output)

    if input_argument:
        if hasattr(gh, input_argument):
            method = getattr(gh, input_argument)
            if method:
                method()
                return
        github_name = input_argument.lower()
        storage.set_hash_value("github:users", bot_input.nick, github_name)
    else:
        github_name = storage.get_hash_value("github:users", bot_input.nick)

    if not github_name:
        bot_output.say("Who the hell are you?  Try .github <username>.  And if you pass in angle brackets I will return you to sender, postage unpaid.")
        return

    gh.pull_requests(github_name)


@hook.regex(r'create pull request (?P<branch>.*)', run_always=True)
def create_pull_request(bot_input, bot_output):
    branch = bot_input.groupdict()["branch"]
    helper = Github_Helper(bot_input, bot_input)
    github = Github(bot_input.bot.credentials["github"]["login"], bot_input.bot.credentials["github"]["password"])
    org = github.get_organization("daptiv")
    repo = org.get_repo("Ppm")
    master_branch = "master"

    new_pull_request = repo.create_pull(title=branch, body='\n'.join(helper.get_team_members()), base=master_branch, head=branch)

    bot_output.say(new_pull_request.url)


class Github_Helper(object):
    def __init__(self, bot_input, bot_output):
        self.bot_input = bot_input
        self.bot_output = bot_output

    def pull_requests(self, github_name):
        github = Github(self.bot_input.bot.credentials["github"]["login"], self.bot_input.bot.credentials["github"]["password"])
        org = github.get_organization("daptiv")
        repos = org.get_repos()
        found_pull_requests = False
        self.bot_output.say(random.choice(self.bot_output.responses["github"]).format(self.bot_input.nick))

        for repo in repos:
            pull_requests = self.get_pull_requests(repo, github_name)
            if pull_requests:
                self.bot_output.say('\n'.join(pull_requests))
                found_pull_requests = True

        if found_pull_requests:
            self.bot_output.say('Think I got them all. Good luck with that.')
        else:
            self.bot_output.say(random.choice(self.bot_output.responses["nothing_for_you"]))

    def get_team_members(self):
        github = Github(self.bot_input.bot.credentials["github"]["login"], self.bot_input.bot.credentials["github"]["password"])
        org = github.get_organization("daptiv")
        team = org.get_teams()
        results = []

        for t in team:
            if t.name.lower() == self.bot_output.team_name.lower():
                for homie in t.get_members():
                        results.append(" - [ ] @{0}".format(homie.login))
        return results

    def teampr(self):
        ".teampr [teamname] -- gives a list of pending pull requests for user. Ommitting teamnames uses last one passed in"

        self.bot_output.say(random.choice(self.bot_output.responses["github"]).format(self.bot_input.nick))

        github = Github(self.bot_input.bot.credentials["github"]["login"], self.bot_input.bot.credentials["github"]["password"])
        org = github.get_organization("daptiv")
        team = org.get_teams()

        for t in team:
            if t.name.lower() == self.bot_output.team_name.lower():
                team_repos = t.get_repos()
                team_members = t.get_members()
                for repo in team_repos:
                    for member in team_members:
                        pull_requests = self.display_pull_requests_for_team_member(repo, member)
                        if pull_requests:
                            self.bot_output.say("Open Pull Requests for " + member.login)
                            self.bot_output.say('\n'.join(pull_requests))

    def teamstatus(self):

        github = Github(self.bot_input.bot.credentials["github"]["login"], self.bot_input.bot.credentials["github"]["password"])
        org = github.get_organization("daptiv")
        team = org.get_teams()

        for t in team:
            if t.name.lower() == self.bot_output.team_name.lower():
                team_repos = t.get_repos()
                team_members = t.get_members()
                for repo in team_repos:
                    for member in team_members:
                        pull_requests = self.get_pull_requests_for_team_member(repo, member)
                        pull_requests = self.get_unreviewed_pull_requests(pull_requests)
                        if pull_requests:
                            self.bot_output.say("Open Pull Requests for " + member.login)
                            self.bot_output.say('\n'.join(pull_requests))

    def get_pull_requests_by_team(self, repo):
        results = []
        open_pull_requests = repo.get_pulls("open")
        if open_pull_requests:
            for pull in open_pull_requests:
                if pull.body in pull.body:
                    results.append("{0} - {1}".format(pull.title, pull.html_url))
        return results

    def get_pull_requests(self, repo, github_name):
        results = []
        search_string = "[ ] @{0}".format(github_name)
        open_pull_requests = repo.get_pulls("open")
        if open_pull_requests:
            for pull in open_pull_requests:
                if pull.body and search_string in pull.body:
                    results.append("{0} - {1}".format(pull.title, pull.html_url))
        return results

    def display_pull_requests_for_team_member(self, repo, team_member):
        results = []
        open_pull_requests = repo.get_pulls("open")
        if open_pull_requests:
            for pull in open_pull_requests:
                if pull.body and pull.user == team_member:
                    results.append(" - {0} - {1}".format(pull.title, pull.html_url))
        return results

    def get_pull_requests_for_team_member(self, repo, team_member):
        results = []
        open_pull_requests = repo.get_pulls("open")
        if open_pull_requests:
            for pull in open_pull_requests:
                if pull.body and pull.user == team_member:
                    results.append(pull)
        return results

    def get_unreviewed_pull_requests(self, pull_requests):
        results = []
        if pull_requests:
            for pull in pull_requests:
                if pull.body:
                    match = re.findall('(?<=\[ \] @)(\w+)', pull.body)
                    results.append("{0} - {1}".format(pull.title, pull.html_url))
                    for homie in match:
                        results.append(" - [ ] @{0}".format(homie))
        return results
    
    def get_stand_up_by_user(self, user):
        # Hardcode repos for now
        gi = Github(self.bot_input.bot.credentials["github"]["login"], self.bot_input.bot.credentials["github"]["password"])
        org = gi.get_organization("daptiv")
        teams = org.get_teams()
        pull_requests = []

        for t in teams:
            if t.name.lower() == self.bot_output.team_name.lower():
                team_repos = t.get_repos()
                team_members = t.get_members()
                for repo in team_repos:
                    for member in team_members:
                        if member.login == user:
                            pull_requests.append(self.get_pull_requests_for_team_member(repo, member))

        return pull_requests

