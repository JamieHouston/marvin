import redis

server = redis.StrictRedis(host='localhost', port=6379, db=0)


def has_key(key):
    return server.exists(key)


def get_value(key):
    return server.get(key)


def set_value(key, value):
    server.set(key, value)


def add_to_list(key, value):
    server.sadd(key,value)


def get_list(key):
    return server.smembers(key)


def delete_from_list(key, value):
    server.srem(key, value)


def get_server():
    return server

def get_random_value(key):
    return server.srandmember(key)


def get_hash_value(hash_list_name, hash_key):
    return server.hget(hash_list_name, hash_key)


def set_hash_value(hash_list_name, key, value):
    server.hset(hash_list_name, key, value)


def delete_hash_value(hash_list_name, key):
    server.hdel(hash_list_name, key)