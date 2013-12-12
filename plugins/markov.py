# #!/usr/bin/python
# import random
# import re
# from util import storage, hook
#
# chain_length = 2
# chattiness = .1
# max_words = 30
# messages_to_generate = 5
# prefix = 'markov'
# separator = '\x01'
# stop_word = '\x02'
#
# def make_key(k, nick):
#     return '-'.join((prefix, nick, k)).lower()
#
# def sanitize_message(message):
#     return re.sub('[\"\']', '', message.lower())
#
# def split_message(message):
#     # split the incoming message into words, i.e. ['what', 'up', 'bro']
#     words = message.split()
#
#     # if the message is any shorter, it won't lead anywhere
#     if len(words) > chain_length:
#
#         # add some stop words onto the message
#         # ['what', 'up', 'bro', '\x02']
#         words.append(stop_word)
#
#         # len(words) == 4, so range(4-2) == range(2) == 0, 1, meaning
#         # we return the following slices: [0:3], [1:4]
#         # or ['what', 'up', 'bro'], ['up', 'bro', '\x02']
#         for i in range(len(words) - chain_length):
#             yield words[i:i + chain_length + 1]
#
# def generate_message(seed, nick):
#     key = seed
#
#     # keep a list of words we've seen
#     gen_words = []
#
#     # only follow the chain so far, up to <max words>
#     for i in xrange(max_words):
#
#         # split the key on the separator to extract the words -- the key
#         # might look like "this\x01is" and split out into ['this', 'is']
#         words = key.split(separator)
#
#         # add the word to the list of words in our generated message
#         gen_words.append(words[0])
#
#         # get a new word that lives at this key -- if none are present we've
#         # reached the end of the chain and can bail
#         next_word = storage.server.srandmember(make_key(key, nick))
#         if not next_word:
#             break
#
#         # create a new key combining the end of the old one and the next_word
#         key = separator.join(words[1:] + [next_word])
#
#     return ' '.join(gen_words)
#
# def log(bot_input, bot_output):
#     # speak only when spoken to, or when the spirit moves me
#     say_something = random.random() < chattiness
#
#     messages = []
#
#     # use a convenience method to strip out the "ping" portion of a message
#     message = bot_input.message
#     if not message or message.startswith('/'):
#         return
#
#     starter = message.split()[0]
#
#     storage.server.sadd(make_key("words", bot_input.nick), starter)
#     # split up the incoming message into chunks that are 1 word longer than
#     # the size of the chain, e.g. ['what', 'up', 'bro'], ['up', 'bro', '\x02']
#     for words in split_message(sanitize_message(message)):
#         # grab everything but the last word
#         key = separator.join(words[:-1])
#
#         # add the last word to the set
#         storage.server.sadd(make_key(key, bot_input.nick), words[-1])
#
#         # if we should say something, generate some messages based on what
#         # was just said and select the longest, then add it to the list
#     if say_something:
#         imitate(bot_input, bot_output)
#
#
# @hook.regex(r'imitate( )?(?P<name>[\w]*)')
# def imitate(bot_input, bot_output):
#     if hasattr(bot_input, 'groupdict') and bot_input.groupdict():
#         person_name = bot_input.groupdict()["name"]
#     else:
#         person_name = bot_input.nick
#
#     key = make_key("words", person_name)
#
#     first_word = storage.server.srandmember(key)
#
#     best_message = ''
#     for i in range(messages_to_generate):
#         generated = generate_message(seed=first_word, nick = person_name)
#         if len(generated) > len(best_message):
#             best_message = generated
#
#     if best_message:
#         bot_output.say(best_message)
#     else:
#         bot_output.say("Can't touch that.")
