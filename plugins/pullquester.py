import shlex
from plugins.gitty import GithubHelper
from plugins.target_process import TargetProcess

from util import hook, userinfo

@hook.regex("create a pull request for (?P<story_number>[\w]*)")
def personal_pull_request(bot_input, bot_output):

    pull_request(bot_input, bot_output)

@hook.command
def pull_request(bot_input, bot_output):
    """.pull_request [story number] -- creates a pull request for branch with story number
Create a pull request for [story number] -- creates a pull request for branch with story number """

    if hasattr(bot_input, 'groupdict'):
        story_number = bot_input.groupdict()["story_number"]
    else:
        story_number = bot_input.input_string

    if not story_number:
        bot_output.say("Not sure what story number you're asking me to create a pull request for...")
        return

    tp = TargetProcess(bot_input, bot_output)

    pull_request_url = None
    team_name = userinfo.get_user_team(bot_input.nick)

    if not team_name:
        bot_output.say("Not sure what team you're on {0}.  Try telling me by saying 'I'm on team [team name]'"
                       .format(bot_input.nick))
        return

    # Get stories in TP by story number
    stories = tp.get_stories_by_team(team_name, ('In Progress', 'In Review'))
    matching_stories = [story for story in stories["Items"] if story_number in str(story["Id"])]
    if len(matching_stories) == 1:
        matching_story = matching_stories[0]
        pull_request_url = create_pull_request(bot_input, bot_output, matching_story)
    else:
        bot_output.say("Found {0} stories for {1} so I can't create a PR".format(len(matching_stories), story_number))
    # elif cmd == "user":
    #     # Get stories in TP by user
    #     stories = tp.get_stories_by_user(cmd_parameter)
    #     if len(stories) == 1:
    #         matching_story = stories[0]
    #         bot_output.say("Creating PR for {0}".format(matching_story["Name"]))
    #         pull_request_url = create_pull_request(bot_input, bot_output, stories[0])
    #     else:
    #         bot_output.say("Found {0} stories for {1} so I can't create a PR".format(len(stories), cmd_parameter))

    if matching_story and pull_request_url:
        tp.create_task(story_number, pull_request_url)
        tp.update_story_state(story_number, "Ready for Review")
        bot_output.say("Task added to story {0}".format(matching_story["Id"]))


def create_pull_request(bot_input, bot_output, story):
    story_number = str(story["Id"])
    url = "https://daptiv.tpondemand.com/entity/{0}".format(story_number)
    bot_output.say("Creating PR for [{0}]({1})".format(story["Name"], url))

    gh = GithubHelper(bot_input, bot_output)

    new_pull_request = gh.create_pull_request_from_partial_name(story_number)
    if new_pull_request:
        response = "PR for branch {0} created - [{1}]({2})".format(
            new_pull_request.title, new_pull_request.title, new_pull_request.html_url)
        bot_output.say(response)
        return new_pull_request.html_url
    else:
        bot_output.say("No branch found for story {0}".format(story_number))
    # Create PR if there's only 1

    # Attach task to story with PR url
