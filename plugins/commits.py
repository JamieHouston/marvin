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

def get_commits(bot_input, bot_output):
    gh = GithubHelper(bot_input, bot_output)
    team = gh.get_team()
    team_repos = team.get_repos()
    random_repo = team_repos[random.randrange(0,3)]
    start_date = moment.now().add(key='days',amount=-30).date
    commits = random_repo.get_commits(since=start_date)
    return commits


@hook.command
def commit(bot_input, bot_output):
    """
    .commit - display a random commit message
    .commit <username> - guess who said the commit
    .commit answer - show the answer and link
    """
    global last_commit
    user_input = bot_input.input_string
    if user_input and last_commit is not None:
        answer = "It was {0} ({1}\n{2}".format(last_commit.author.login, last_commit.author.name, last_commit.html_url)
        if user_input.lower() == "answer":
            bot_output.say(answer)
        else:
            guess = user_input.replace('@', '').lower()
            if guess in last_commit.author.name.lower() or guess in last_commit.author.login:
                bot_output.say("Correct! {0}".format(answer))
            else:
                bot_output.say("Not even close, {0}")
    else:
        commits = get_commits(bot_input, bot_output)
        last_commit = commits[random.randrange(100)]

        bot_output.say("Who said:\n{0})".format(last_commit.commit.message))
