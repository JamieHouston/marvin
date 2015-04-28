from apis.teamcity.api import TeamCityRESTApiClient
from util import hook


def get_tc_client(credentials):
    # TODO: Make client singleton
    api_client = TeamCityRESTApiClient(
        credentials["team_city"]["login"],
        credentials["team_city"]["password"],
        credentials["team_city"]["server"]
    )

    return api_client

@hook.regex(r'(show all projects)', run_always=True)
def teamcity(bot_input, bot_output):
    bot_output.say("that's a long list, but here goes....")
    tc_client = get_tc_client(bot_input.bot.credentials)
    tc_client.get_all_projects()
    data = tc_client.get_from_server()

    for project in data['project']:
        bot_output.say(project['name'])


@hook.regex('tc build (?P<build_id>\d+)', run_always=True)
def tc_status(bot_input, bot_output):
    input_argument = bot_input.inp["build_id"]

    if input_argument:
        bot_output.say("looking for build " + input_argument)
        tc_client = get_tc_client(bot_input.bot.credentials)
        tc_client.get_build_by_build_id(input_argument)
        data = tc_client.get_from_server()
        bot_output.say(data['statusText'])
    else:
        bot_output.say("You didn't pass a build id")

@hook.regex('tc status (?P<project_name>.*)')
def project_status(bot_input, bot_output):
    input_argument = bot_input.inp["build_id"]
    if not input_argument:
        teamcity(bot_input, bot_output)
        return

    project_name = input_argument.lower()
    bot_output.say("Getting status of {0}".format(project_name))
    tc_client = get_tc_client(bot_input.bot.credentials)

    project_info = tc_client.get_project_by_project_id(project_name)
    if project_info:
        bot_output.say(project_info[""])