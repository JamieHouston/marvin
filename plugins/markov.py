# #!/usr/bin/python
# import random
# from util import storage, textutils
#
# chain_length = 2
# max_words = 30
# messages_to_generate = 5
# prefix = 'markov'
# separator = '\x01'
# stop_word = '\x02'
#
#
# def make_key(k):
#     return '-'.join((prefix, k))
#
#
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
#
# def generate_message(seed):
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
#         next_word = storage.get_random_value(make_key(key))
#         if not next_word:
#             break
#
#         # create a new key combining the end of the old one and the next_word
#         key = separator.join(words[1:] + [next_word])
#
#     return ' '.join(gen_words)
#
#
# def handle(bot_input, bot_output):
#     # speak only when spoken to, or when the spirit moves me
#     say_something = random.random() < (bot_output.chattiness / 10)
#
#     messages = []
#
#     message = bot_input.message
#
#     # use a convenience method to strip out the "ping" portion of a message
#     if message.startswith('/'):
#         return
#
#     # split up the incoming message into chunks that are 1 word longer than
#     # the size of the chain, e.g. ['what', 'up', 'bro'], ['up', 'bro', '\x02']
#     for words in split_message(textutils.sanitize_message(message)):
#         # grab everything but the last word
#         key = separator.join(words[:-1])
#
#         # add the last word to the set
#         storage.add_to_list(make_key(key), words[-1])
#
#         # if we should say something, generate some messages based on what
#         # was just said and select the longest, then add it to the list
#         if say_something:
#             best_message = ''
#             for i in range(messages_to_generate):
#                 generated = generate_message(seed=key)
#                 if len(generated) > len(best_message):
#                     best_message = generated
#
#             if best_message:
#                 messages.append(best_message)
#
#     if len(messages):
#         bot_output.say(random.choice(messages))
