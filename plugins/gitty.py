from util import hook, storage
from github import Github
import random
import re

@hook.command
def github(bot_input, bot_output):
    """.github [username] -- gives a list of pending pull requests for user. Omitting username uses last one passed in
    .github teamstatus -- gives a list of pending pull requests for user. Omitting teamnames uses last one passed in"""

    input_argument = bot_input.input_string

    gh = GithubHelper(bot_input, bot_output)

    if input_argument:
        if hasattr(gh, input_argument):
            method = getattr(gh, input_argument)
            if method:
                method()
                return
        github_name = input_argument.lower()

    if not github_name:
        bot_output.say("Who the hell are you?  Try .github <username>.\
          And if you pass in angle brackets I will return you to sender, postage unpaid.")
        return

    bot_output.say(random.choice(bot_output.responses["github"]))

    pull_requests = gh.pull_requests(github_name)

    for pull_request in pull_requests:
        formatt_request = "[{0}]({1})".format(pull_request.title, pull_request.html_url)
        bot_output.say(formatt_request)

    bot_output.say('All done {0}. Good luck with that.')


@hook.regex(r'create pull request (?P<branch>.*)', run_always=True)
def create_pull_request(bot_input, bot_output):
    branch = bot_input.groupdict()["branch"]
    helper = GithubHelper(bot_input, bot_input)
    github_api = Github(bot_input.bot.credentials["github"]["login"], bot_input.bot.credentials["github"]["password"])
    org = github_api.get_organization("daptiv")
    repo = org.get_repo("Ppm")
    master_branch = "master"

    team = helper.get_team()
    random_member = random.choice(team.get_members())
    body = " - [ ] @{0}".format(random_member.login)

    new_pull_request = repo.create_pull(title=branch, body=body, base=master_branch,
                                        head=branch)

    bot_output.say(new_pull_request.url)


class GithubHelper(object):
    def __init__(self, bot_input, bot_output):
        self.bot_input = bot_input
        self.bot_output = bot_output

        # TODO: Get org from config
        self.organization = "daptiv"
        self.team_name = self.bot_output.team_name.lower()

        self.github_api = Github(
            self.bot_input.bot.credentials["github"]["login"],
            self.bot_input.bot.credentials["github"]["password"])

    def get_organization(self):
        return self.github_api.get_organization(self.organization)

    def pull_requests(self, github_name):
        team = self.get_team()
        if team:
            repos = team.get_repos()
        else:
            org = self.get_organization()
            repos = org.get_repos()

        for repo in repos:
            yield from self.get_unchecked_pull_requests_for_user(repo, github_name)

    def get_team(self):
        org = self.get_organization()
        teams = org.get_teams()

        team = [team for team in teams if team.name.lower() == self.team_name]
        if len(team):
            return team[0]

    def teampr(self):
        """.teampr [teamname] -- gives a list of pending pull requests for user."""

        self.bot_output.say(random.choice(self.bot_output.responses["github"]).format(self.bot_input.nick))

        team = self.get_team()

        team_repos = team.get_repos()
        team_members = team.get_members()
        for repo in team_repos:
            for member in team_members:
                pull_requests = self.display_pull_requests_for_team_member(repo, member)
                if pull_requests:
                    self.bot_output.say("Open Pull Requests for " + member.login)
                    self.bot_output.say('\n'.join(pull_requests))

    def teamstatus(self):

        github_api = Github(self.bot_input.bot.credentials["github"]["login"],
                            self.bot_input.bot.credentials["github"]["password"])
        org = github_api.get_organization("daptiv")
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

    def get_unchecked_pull_requests_for_user(self, repo, github_name):
        search_string = "[ ] @{0}".format(github_name)
        open_pull_requests = repo.get_pulls("open")
        if open_pull_requests:
            for pull in open_pull_requests:
                if pull.body and search_string in pull.body:
                    yield pull

    def display_pull_requests_for_team_member(self, repo, team_member):
        results = []
        user_pulls = self.get_pull_requests_for_team_member(repo, team_member)
        for pull in user_pulls:
            results.append(" - {0} - {1}".format(pull.title, pull.html_url))
        return results

    def get_pull_requests_for_team_member(self, repo, team_member):
        open_pull_requests = repo.get_pulls("open")
        if open_pull_requests:
            return [pull_request for pull_request in open_pull_requests if pull_request.user == team_member]
        return []

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
        github_api = Github(self.bot_input.bot.credentials["github"]["login"],
                    self.bot_input.bot.credentials["github"]["password"])
        org = github_api.get_organization("daptiv")
        teams = org.get_teams()
        pull_requests = []

        for t in teams:
            if t.name.lower() == self.bot_output.team_name.lower():
                team_repos = t.get_repos()
                team_members = t.get_members()
                for repo in team_repos:
                    for member in team_members:
                        if member.login == user:
                            pull_requests += self.display_pull_requests_for_team_member(repo, member)

        return pull_requests

