from util import hook, web
import json
import textwrap
import datetime
import shlex
from urllib import parse

"""
Main command
Loads config named "target_process"
"""


@hook.command
def target_process(bot_input, bot_output):
    """.target_process id [story id] -- gives details on the story\n.
    target_process su [tp name] - gives updates on the user\n.
    target_process team [team name] - show stories for the team that haven't changed in a day"""
    user_input = bot_input.input_string
    user_input = shlex.split(user_input)
    output_string = "I don't recognize that command, {0}.\nTry .help target_process"
    tp = TargetProcess(bot_input, bot_output)

    if len(user_input) > 1:
        cmd = user_input[0]
        cmd_parameter = user_input[1]
        if cmd == "id":
            output_string = tp.get_story_by_id(cmd_parameter)
        elif cmd == "su":
            output_string = tp.get_stand_up_by_user(cmd_parameter)
        elif cmd == "team":
            output_string = tp.get_stories_by_team(cmd_parameter)
        elif cmd == "task":
            output_string = tp.create_task(cmd_parameter, "test task for " + cmd_parameter)

    bot_output.say(output_string)

"""
https://md5.tpondemand.com/api/v1/index/meta
"""


class TargetProcess():
    user = ''
    tp_uri = ''
    token = ''

    def __init__(self, bot_input, bot_output):
        url = bot_input.bot.credentials["target_process"]["url"]
        token = bot_input.bot.credentials["target_process"]["token"]

        self.data = []
        self.tp_uri = url
        self.token = token

    def get_object(self, api_suffix):
        auth_token = "&token=%s" % self.token
        request_string = self.tp_uri + api_suffix + "&format=json" + auth_token

        print(request_string)

        return web.get_text(request_string)

    def create_task(self, story_number, task_title):
        body = {"Name": task_title, "UserStory": {"Id": story_number}}
        url = "{0}{1}?token={2}&format=json".format(self.tp_uri, "tasks", self.token)
        result = web.post_json(url, body)
        return result

    def update_story_state(self, story_number, new_state):
        # TODO: Grab this from API!
        entity_states = {
            'in review': 438
        }
        entity_state_id = entity_states[new_state.lower()]

        body = {"Id": story_number, "EntityState": {"Id": entity_state_id}}
        url = "{0}{1}?token={2}&format=json".format(self.tp_uri, "userstories", self.token)
        result = web.post_json(url, body)
        return result

    # Functions that fetch objects
    def get_user_stories(self, login, entity_state, date_modified=''):
        where = "(AssignedUser.Login eq '" + login + "')"
        where += "and (EntityState.Name in ('" + '\', \''.join(entity_state) + "'))"
        if date_modified:
            where += "and (ModifyDate gte " + date_modified.strftime("'%Y-%m-%d'") + ")"
        query = "UserStories?include=[Name,EntityState,ModifyDate,Effort,Tasks]&where=" + parse.quote_plus(where)
        result = self.get_object(query)
        return json.loads(result)["Items"]

    # https://md5.tpondemand.com/api/v1/TaskHistories/meta
    def get_task_history(self, task_ids, days_edited_ago):
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=days_edited_ago)
        where = "(Date gte %s)" % yesterday.strftime("'%Y-%m-%d'")
        where += "and (Task.Id in (%s))" % ", ".join(str(tid) for tid in task_ids)
        where = parse.quote_plus(where)
        result = self.get_object("TaskHistories?include=[Date,EntityState,Modifier,Task]&where=" + where)
        return json.loads(result)["Items"]

    # Shared formatting for story string
    def get_story_string(self, user_story):
        story_id = str(user_story["Id"])
        padding = " " * len(story_id + " - ")
        return "\n\t" + ("\n\t" + padding).join(textwrap.wrap(story_id + " - " + user_story["Name"]
                                                              + " [" + str(user_story["Effort"]) + "pt, " +
                                                              user_story["EntityState"]["Name"] + "]", 80)) + "\n"

    def get_stories_by_team(self, team_name, active_states):
        where = "(Team.Name eq '" + team_name + "')" \
                + "and (EntityState.Name in ('" + '\', \''.join(active_states) + "'))"

        query = "UserStories?include=[Name,EntityState,LastStateChangeDate,Effort]&where=" + parse.quote_plus(where)
        result = json.loads(self.get_object(query))
        return result


    """
    Functions that return strings (bot output)
    """

    def get_stories_by_team_description(self, team_name):
        stories = []

        today = datetime.datetime.today()

        active_states = ('In Progress', 'In Review', 'Testing', 'Blocked', 'Done')
        stories = self.get_stories_by_team_description(team_name, active_states)

        for user_story in stories["Items"]:
            last_changed = json_date_as_datetime(user_story["LastStateChangeDate"])
            if (today - last_changed).days > 1:
                stories.append("Last Changed: " + last_changed.strftime("'%m-%d-%Y %H:%M'"))
                stories.append(self.get_story_string(user_story))
        return '\n'.join(stories)

    def get_stories_by_user(self, login):
        output_string = ""
        stories = self.get_user_stories(login, 'In Progress')
        for user_story in stories:
            output_string += self.get_story_string(user_story)

        return output_string

    def get_story_by_id(self, story_id):
        output_string = ""
        where = parse.quote_plus("(Id eq '" + story_id + "')")
        query = "UserStories?include=[Name,EntityState,ModifyDate,Effort]&where=" + where
        story_data = self.get_object(query)
        result = json.loads(story_data)

        for user_story in result["Items"]:
            output_string += self.get_story_string(user_story)
        if not output_string:
            output_string = "Story not found: " + story_id

        return output_string

    def get_stand_up_by_user(self, login):
        # Get all stories for user
        # Get all tasks
        # Get history of tasks
        # Display any changes done to tasks yesterday
        # Determine what in progress means based on role of assigned user
        output_string = ""

        # how many days into the past to check
        days_previous = 2

        # TODO: change based on the user type
        stories = self.get_user_stories(
            login,
            ('In Progress', 'In Review', 'Accepted'),
            datetime.date.today() - datetime.timedelta(days=days_previous))

        # print all stories and tasks edited in the last n days
        for user_story in stories:
            output_string += self.get_story_string(user_story)

            task_ids = []
            for task in user_story['Tasks']['Items']:
                task_ids.append(task["Id"])

            task_history = self.get_task_history(task_ids, days_previous)
            # history_list = []
            for history in task_history:
                #history_list.append(['Task']['Id'])
                #history_list[history['Task']['Id']][history["Modifier"]["Id"]]['EntityState'].append(history["EntityState"]["Name"])

                output_string += "\t\t" \
                                 + json_date_as_datetime(history["Date"]).strftime("%d-%b-%Y") \
                                 + "\t " + history['Modifier']['FirstName'] \
                                 + "\t " + history["EntityState"]["Name"] \
                                 + "\t\t " + history["Task"]["Name"] \
                                 + "\n"

        return output_string


# Utilities
# http://stackoverflow.com/questions/5786448/date-conversion-net-json-to-iso
def json_date_as_datetime(jd):
    sign = jd[-7]
    if sign not in '-+' or len(jd) == 13:
        ms = int(jd[6:-2])
    else:
        ms = int(jd[6:-7])
        hh = int(jd[-7:-4])
        mm = int(jd[-4:-2])
        if sign == '-': mm = -mm
        ms += (hh * 60 + mm) * 60000
    return datetime.datetime(1970, 1, 1) \
           + datetime.timedelta(microseconds=ms * 1000)

