from apis.teamcity.api import TeamCityRESTApiClient
from util import hook

@hook.regex(r'(show all projects)', run_always=True)
def teamcity(bot_input, bot_output):
    bot_output.say("that's a long list, but here goes....")
    tc = TeamCityRESTApiClient(bot_input.bot.credentials["team_city"]["login"], bot_input.bot.credentials["team_city"]["password"], bot_input.bot.credentials["team_city"]["server"])
    tc.get_all_projects()
    data = tc.get_from_server()

    for project in data['project']:
        bot_output.say(project['name'])


@hook.regex('tc build (?P<build_id>\d+)', run_always=True)
def tc_status(bot_input, bot_output):
    input_argument = bot_input.inp["build_id"]

    if input_argument:
        bot_output.say("looking for build " + input_argument)
        tc = TeamCityRESTApiClient(bot_input.bot.credentials["team_city"]["login"], bot_input.bot.credentials["team_city"]["password"], bot_input.bot.credentials["team_city"]["server"])
        tc.get_build_by_build_id(input_argument)
        data = tc.get_from_server()
        bot_output.say(data['statusText'])
    else:
        bot_output.say("You didn't pass a build id")