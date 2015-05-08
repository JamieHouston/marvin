from util import hook, userinfo
from github import Github
import random
import re


@hook.command
def github(bot_input, bot_output):
    """.github [username] -- gives a list of pending pull requests for user. Omitting username uses nick of user making request
.github teamstatus -- gives a list of pending pull requests for user."""

    input_argument = bot_input.input_string

    gh = GithubHelper(bot_input, bot_output)
    github_name = bot_input.nick

    if input_argument:
        if hasattr(gh, input_argument):
            method = getattr(gh, input_argument)
            if method:
                method()
                return
        github_name = input_argument.lower()

    bot_output.say(random.choice(bot_output.responses["github"]))

    pull_requests = gh.pull_requests(github_name)

    for pull_request in pull_requests:
        format_request = "[{0}]({1})".format(pull_request.title, pull_request.html_url)
        bot_output.say(format_request)

    bot_output.say('All done {user_nick}. Good luck with that.')


@hook.regex(r'create pull request (?P<branch>.*)', run_always=True)
def create_pull_request(bot_input, bot_output):
    branch = bot_input.groupdict()["branch"]
    helper = GithubHelper(bot_input, bot_input)
    new_pull_request = helper.create_pull_request(branch)
    bot_output.say(new_pull_request.url)


class GithubHelper(object):
    def __init__(self, bot_input, bot_output):
        self.bot_input = bot_input
        self.bot_output = bot_output

        # TODO: Get org from config
        self.organization = "daptiv"
        self.team_name = userinfo.get_user_team(bot_input.nick) or self.bot_output.team_name.lower()

        self.github_api = Github(
            self.bot_input.bot.credentials["github"]["login"],
            self.bot_input.bot.credentials["github"]["password"])

    def create_pull_request_from_partial_name(self, branch_name):
        branch, repo = self.get_branch_and_repo(branch_name)
        if branch and repo:
            return self.create_pull_request(repo, branch)
        return None

    def create_pull_request(self, repo, branch):
        # TODO: This should be stored in userinfo as well, so it works in flowdock
        # Add command to "my github username is [username] or something

        github_name = self.bot_input.nick
        master_branch = "master"

        # TODO: This doesn't guarantee the story number - only if it's 12345-story-name
        story_number = branch.name.split('-')[0]
        team_members = userinfo.get_user_team_members(github_name)

        random_member = random.choice(
            [member for (member, role) in team_members.items() if role == "developer" and member != github_name])
        testers = [member for (member, role) in team_members.items() if role == "tester"]

        tc_test_url = \
            "http://teamcity.hq.daptiv.com/project.html?projectId=PpmFeatureBranches&tab=projectOverview&branch_PpmFeatureBranches={0}" \
                .format(branch.name)

        tp_story_url = "https://daptiv.tpondemand.com/entity/{0}".format(story_number)

        body = "{0}\n" \
               "=== Code Review ===\n" \
               " - [ ] @{1}\n" \
               " - [ ] [Teamcity Tests Pass]({2})\n\n" \
               "=== Test ===\n" \
               " - [ ] @{3}\n\n" \
               "=== Additional === \n" \
               " - [ ] [Feature is dev complete]({4})" \
            .format(story_number,
                    random_member,
                    tc_test_url,
                    "| @".join(testers),
                    tp_story_url)

        # TODO: Add link to TC and TP
        new_pull_request = repo.create_pull(title=branch.name, body=body, base=master_branch,
                                            head=branch.name)

        return new_pull_request


    def get_organization(self):
        return self.github_api.get_organization(self.organization)

    # Get all repos for the current team or organization if team isn't available
    def get_repos(self):
        team = self.get_team()
        if team:
            repos = team.get_repos()
        else:
            org = self.get_organization()
            repos = org.get_repos()

        return repos

    # Pass in partial branch name (like story number) and get back branch
    def get_branch_and_repo(self, branch_name):
        repos = self.get_repos()
        for repo in repos:
            branches = repo.get_branches()
            matching_branch = [branch for branch in branches if branch_name in branch.name]
            if matching_branch:
                return matching_branch[0], repo
        return None

    def pull_requests(self, github_name):
        repos = self.get_repos()

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
                    self.bot_output.say("##Open Pull Requests for @" + member.login)
                    self.bot_output.say('\n'.join(pull_requests))

    def teamstatus(self):

        team = self.get_team()

        team_repos = team.get_repos()
        team_members = team.get_members()
        for repo in team_repos:
            for member in team_members:
                team_pull_requests = self.get_pull_requests_for_team_member(repo, member)
                unreviewed_pull_requests = self.get_unreviewed_pull_requests(team_pull_requests)
                if unreviewed_pull_requests:
                    self.bot_output.say("##Open Pull Requests for @" + member.login)
                    self.bot_output.say('\n'.join(unreviewed_pull_requests))

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
            results.append("[{0}]({1})".format(pull.title, pull.html_url))
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
                    results.append("[{0}]({1})".format(pull.title, pull.html_url))
                    for homie in match:
                        results.append(" - [ ] @{0}".format(homie))
        return results

    def get_stand_up_by_user(self, user):
        pull_requests = []
        team = self.get_team()
        team_repos = team.get_repos()
        team_members = team.get_members()
        for repo in team_repos:
            for member in team_members:
                if member.login == user:
                    pull_requests += self.display_pull_requests_for_team_member(repo, member)

        return pull_requests

