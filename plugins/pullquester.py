import shlex
from plugins.gitty import GithubHelper
from plugins.target_process import TargetProcess

from util import hook

@hook.command
def pull_request(bot_input, bot_output):
    """
    .pull_request story [story id] -- creates a pull request for branch with story id (in string search)
    .pull_request user [username] -- creates a pull request for story in dev or review for username (in string search)
    """

    user_input = bot_input.input_string
    user_input = shlex.split(user_input)

    if len(user_input) > 1:
        tp = TargetProcess(bot_input, bot_output)

        cmd = user_input[0]
        cmd_parameter = user_input[1]
        pull_request_url = None
        if cmd == "story":
            team_name = bot_output.team_name.lower()

            # Get stories in TP by story number
            stories = tp.get_stories_by_team(team_name, ('In Progress', 'In Review'))
            matching_stories = [story for story in stories["Items"] if cmd_parameter in str(story["Id"])]
            if len(matching_stories) == 1:
                matching_story = matching_stories[0]
                pull_request_url = create_pull_request(bot_input, bot_output, matching_story)
            else:
                bot_output.say("Found {0} stories for {1} so I can't create a PR".format(len(matching_stories), cmd_parameter))
        elif cmd == "user":
            # Get stories in TP by user
            stories = tp.get_stories_by_user(cmd_parameter)
            if len(stories) == 1:
                matching_story = stories[0]
                bot_output.say("Creating PR for {0}".format(matching_story["Name"]))
                pull_request_url = create_pull_request(bot_input, bot_output, stories[0])
            else:
                bot_output.say("Found {0} stories for {1} so I can't create a PR".format(len(stories), cmd_parameter))

        if matching_story and pull_request_url:
            tp.create_task(matching_story["Id"], pull_request_url)
            bot_output.say("Task added to story {0}".format(matching_story["Id"]))


def create_pull_request(bot_input, bot_output, story):
    story_number = str(story["Id"])
    url = "https://daptiv.tpondemand.com/entity/{0}".format(story_number)
    bot_output.say("Creating PR for [{0}]({1})".format(story["Name"], url))

    gh = GithubHelper(bot_input, bot_output)

    pull_request = gh.create_pull_request_from_partial_name(story_number)
    if pull_request:
        response = "PR for branch {0} created - [{1}]({2})".format(
            pull_request.title, pull_request.title, pull_request.html_url)
        bot_output.say(response)
        return pull_request.html_url
    else:
        bot_output.say("No branch found for story {0}".format(story_number))
    # Create PR if there's only 1

    # Attach task to story with PR url
