from util import hook, userinfo


@hook.regex(r"(?:who is) (?P<username>[\w\d]*)(?:\?)?$")
def who_is_user(bot_input, bot_output):
    """who is [username] -- get information about username"""

    if bot_input.groupdict():
        username = bot_input.groupdict()["username"]
        if username.startswith("who"):
            return
        user_info = userinfo.get_user_info(username)
        results = []
        if user_info:
            results.append("{0} is".format(username))
            if user_info["role"]:
                results.append("a {0}".format(user_info["role"]))
            if user_info["team"]:
                results.append("on team {0}".format(user_info["team"]))
            bot_output.say(" ".join(results))
        else:
            bot_output.say("Never heard of {0}".format(username))
    else:
        bot_output.say("Did you slur?")


@hook.regex(r"(?:who is on) (?:the )?(?:team )?(?P<team_name>[\w\d]*)(?: team)?(?:\?)?")
def who_is_team(bot_input, bot_output):
    """who is [username] -- get information about username"""

    if bot_input.groupdict():
        team_name = bot_input.groupdict()["team_name"]
        team_members = userinfo.get_team_members(team_name)
        if team_members:
            results = []
            for member, role in team_members.items():
                results.append("{0} ({1})".format(member, role))
            bot_output.say(", ".join(results))
        else:
            bot_output.say("Never heard of {0}".format(team_name))
    else:
        bot_output.say("Did you slur?")


@hook.regex(r"i('m| am)(?P<remove_user> not)?(?: a )?(?P<role>[\w]*) on( team)? (?P<team_name>[\w\d]*)")
def i_am(bot_input, bot_output):
    username_is(bot_input, bot_output)

@hook.regex(r'(?P<username>[\w\d]*) is(?P<remove_user> not)?(?: a )?(?P<role>[\w]*) on( team)? (?P<team_name>[\w\d]*)')
def username_is(bot_input, bot_output):
    """
        [username] is on team [team_name] -- specify which team user is on (for github, target process, etc)
        [username] is not on team [team_name] -- remove a user from a team
    """
    input_parameters = bot_input.groupdict()

    if input_parameters:
        username = input_parameters["username"] if "username" in input_parameters else bot_input.nick
        if username.startswith("who"):
            return
        team_name = input_parameters["team_name"]
        role = input_parameters["role"] or "developer"
        if input_parameters["remove_user"]:
            userinfo.remove_team_member(team_name, username)
            message = "I've removed {0} from team {1}".format(username, team_name)
        else:
            userinfo.set_team_info(team_name, username, role)
            userinfo.set_user_info(username, "team", team_name)
            userinfo.set_user_info(username, "role", role)
            message = "I've assigned {0} to team {1} as a {2}".format(username, team_name, role)
    else:
        message = "You need to provide a team name and username for me to do anything about it"

    bot_output.say(message)