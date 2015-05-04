import random
import moment

from util import hook
from util import web
from plugins.gitty import GithubHelper

url = "http://whatthecommit.com/index.txt"
last_commit = None

# @hook.command
# def commit(input, output):
#     """.commit - generate a random commit message"""
#     output.say(web.get_text(url))


@hook.command
def commit(bot_input, bot_output):
    global last_commit
    action = bot_input.input_string
    if action and action.lower() == "answer" and last_commit is not None:
        bot_output.say("It was {0}. {1}".format(last_commit.author.name, last_commit.html_url))
    else:
        gh = GithubHelper(bot_input, bot_output)
        team = gh.get_team()
        team_repos = team.get_repos()
        random_repo = team_repos[random.randrange(0,3)]
        start_date = moment.now().add(key='days',amount=-30).date
        commits = random_repo.get_commits(since=start_date)
        last_commit = commits[random.randrange(100)]

        bot_output.say("Who said:\n{0})".format(last_commit.commit.message))