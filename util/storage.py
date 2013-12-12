import redis

server = redis.StrictRedis(host='localhost', port=6379, db=0)


def has_key(key):
    return server.exists(key)


def get_value(key):
    return server.get(key)


def set_value(key, value):
    server.set(key, value)


def add_to_list(key, value):
    server.lpush(key,value)


def get_list(key):
    return server.lrange(key,0,-1)

def get_server():
    return server