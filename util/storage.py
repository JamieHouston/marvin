import redis

try:
    server = redis.Redis(host='pub-redis-10118.us-east-1-2.4.ec2.garantiadata.com', port=10118, db=0,
                              password="P@ssw0rd", decode_responses=True)
    # server = redis.StrictRedis(host='localhost', port=6379)
    # server.ping()
except:
    server = None


def has_key(key):
    if server:
        return server.exists(key.lower())
    return False


def get_value(key):
    if server:
        return server.get(key.lower())
    return None


def set_value(key, value):
    if server:
        server.set(key.lower(), value)


def add_to_list(key, value):
    if server:
        server.sadd(key.lower(), value)


def get_list(key):
    if server:
        return server.smembers(key.lower())
    return None


def delete_from_list(key, value):
    if server:
        server.srem(key.lower(), value)


def get_server():
    return server


def get_random_value(key):
    if server:
        return server.srandmember(key.lower())
    return None


def get_hash_value(hash_list_name, hash_key):
    if server:
        return server.hget(hash_list_name.lower(), hash_key.lower())
    return None


def get_hash(hash_list_name):
    if server:
        return server.hgetall(hash_list_name.lower())


def set_hash_value(hash_list_name, key, value):
    if server:
        server.hset(hash_list_name.lower(), key.lower(), value)


def delete_hash_value(hash_list_name, key):
    if server:
        server.hdel(hash_list_name.lower(), key.lower())


def get_hash_keys(hash_list_name):
    if server:
        return server.smembers(hash_list_name.lower())