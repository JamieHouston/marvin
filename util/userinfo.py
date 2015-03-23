from util import storage


def get_user_key(username):
    return "info:username:{0}".format(username)


def get_user_info(username):
    return storage.get_hash(get_user_key(username))


def set_user_info(username, key, value):
    storage.set_hash_value(get_user_key(username), key, value)


def get_team_key(team_name):
    return "info:team:{0}".format(team_name)


def get_team_members(team_name):
    return storage.get_hash(get_team_key(team_name))


def set_team_info(team_name, username, role):
    storage.set_hash_value(get_team_key(team_name), username, role)


def remove_team_member(team_name, username):
    storage.delete_hash_value(get_team_key(team_name), username)


def get_user_team(username):
    user_info = get_user_info(username)
    if user_info and "team" in user_info:
        return user_info["team"]

def get_user_team_members(username):
    team = get_user_team(username)
    if team:
        members = get_team_members(team)
        return members
        #members_except_user = [(member, role) in members.items() if member is not username]