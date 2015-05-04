import random
import moment

from util import hook
from util import web
from plugins.gitty import GithubHelper

url = "http://whatthecommit.com/index.txt"

# @hook.command
# def commit(input, output):
#     """.commit - generate a random commit message"""
#     output.say(web.get_text(url))


@hook.command
def commit(bot_input, bot_output):
    gh = GithubHelper(bot_input, bot_output)
    team = gh.get_team()
    team_repos = team.get_repos()
    random_repo = team_repos[random.randrange(0,3)]
    start_date = moment.now().add(key='days',amount=-30).date
    commits = random_repo.get_commits(since=start_date)
    random_commit = commits[random.randrange(100)]

    bot_output.say("Who said:\n[{0}]({1})".format(random_commit.commit.message, random_commit.url))