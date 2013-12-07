import random
from util import hook, storage

@hook.regex(r'(add )(?P<item>[\w\d\s]*)( to )(the |my )?(?P<list>[\w\d]*)( list)?')
def add_to_list(input, output):
    if input.groupdict():
        item = input.groupdict()["item"]
        list_name = input.groupdict()["list"]
        #if storage.has_key(list_name):
        storage.add_to_list(list_name, item)
        #else:
        #    list_items[list_name] = [item]
        output.say("Added %s to %s choices" % (item, list_name))

@hook.regex(r'(what\'s|when\'s|when is|get|view|search for|show) (on |my |me |the )*(everything)?(?P<request>[\w\d]*)( list)?')
def search_list(input, output):
    if input.groupdict():
        list_name = input.groupdict()["request"]
        if storage.has_key(list_name):
            output.say(", ".join(storage.get_list(list_name)))
        else:
            output.say("There's as many items on that list as there are friends in your phone.")

@hook.regex(r'(pick|decide|where) (something )?(from| on |my |me |the )*(everything)?(?P<request>[\w\d]*)( list)?')
def show_random_list_item(input, output):
    if input.groupdict():
        list_name = input.groupdict()["request"]
        if storage.has_key(list_name):
            result = random.choice(storage.get_list(list_name))
            output.say("I pick %s" % result)
        else:
            output.say("There's as many items on that list as there are friends in your phone.")