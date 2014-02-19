import os,sys
import pickle
import random
import re
from util import hook, textutils


class Markov(object):
    """
    Hacking on a markov chain bot - based on:
    http://code.activestate.com/recipes/194364-the-markov-chain-algorithm/
    http://github.com/ericflo/yourmomdotcom
    """
    messages_to_generate = 5
    max_words = 15
    chain_length = 2
    stop_word = '\n'
    filename = 'markov.db'
    last = None
    activities = 0

    def __init__(self):
        self.load_data()

    def _should_update(self):
        return self.activities > 5

    def load_data(self):
        print "loading data"
        if os.path.exists(self.filename):
            self.word_table = pickle.load(open(self.filename, 'r'))
        else:
            self.word_table = {}

    def _save_data(self):
        #pdb.set_trace()
        print "saving data"
        fh = open(self.filename, 'w')
        fh.write(pickle.dumps(self.word_table))
        fh.close()

    def split_message(self, message):
        words = message.split()
        if len(words) > self.chain_length:
            words.extend([self.stop_word] * self.chain_length)
            for i in range(len(words) - self.chain_length):
                yield (words[i:i + self.chain_length + 1])

    def generate_message(self, person, size=15, seed_key=None):
        person_words = len(self.word_table.get(person, {}))
        if person_words < size:
            return

        if not seed_key:
            seed_key = random.choice(self.word_table[person].keys())

        message = []
        for i in xrange(self.messages_to_generate):
            words = seed_key
            gen_words = []
            for i in xrange(size):
                if words[0] == self.stop_word:
                    break

                gen_words.append(words[0])
                try:
                    words = words[1:] + (random.choice(self.word_table[person][words]),)
                except KeyError:
                    break

            if len(gen_words) > len(message):
                message = list(gen_words)

        return ' '.join(message)

    def imitate(self, bot_input, bot_output):
        person = bot_input.input_string
        if person != bot_output.nick:
            return self.generate_message(person)

    def cite(self, bot_input, bot_output):
        if self.last:
            return self.last

    def is_ping(self, message, bot_output):
        return re.match('^@?%s[:,\s]' % bot_output.nick, message) is not None

    def fix_ping(self, message, bot_output):
        return re.sub('^%s[:,\s]\s*' % bot_output.nick, '', message)

    def log(self, bot_input, bot_output):
        #pdb.set_trace()
        #print >> sys.stderr, "Logging from {0} message: {1}".format(input.nick, input.group(0))
        sender = bot_input.nick[:10]
        message = bot_input.input_string
        self.word_table.setdefault(sender, {})

        if message.startswith('/') or message.startswith('.'):
            return

        try:
            say_something = (not self.is_ping(message, bot_output) and sender != bot_output.nick) and random.random() < bot_output.chattiness
            #print >> sys.stderr, "Say something is: {0}".format(say_something)
        except AttributeError:
            say_something = False
        messages = []
        seed_key = None

        if self.is_ping(message, bot_output):
            message = self.fix_ping(message, bot_output)

        for words in self.split_message(textutils.sanitize_message(message)):
            key = tuple(words[:-1])
            if key in self.word_table:
                self.word_table[sender][key].append(words[-1])
            else:
                self.word_table[sender][key] = [words[-1]]

            if self.stop_word not in key and say_something:
                for person in self.word_table:
                    if person == sender:
                        continue
                    if key in self.word_table[person]:
                        generated = self.generate_message(person, seed_key=key)
                        if generated:
                            messages.append((person, generated))
        self.activities = self.activities + 1

        if self._should_update():
            self._save_data()

        if len(messages):
            self.last, message = random.choice(messages)
            return message

    def load_log_file(self, filename):
        fh = open(filename, 'r')
        logline_re = re.compile('<\s*(\w+)>[^\]]+\]\s([^\r\n]+)[\r\n]')
        for line in fh.readlines():
            match = logline_re.search(line)
            if match:
                sender, message = match.groups()
                self.log(sender, message, '', False, None)
        fh.close()

class BotInfo:
    bot = Markov()

def get_markov():
    return BotInfo.bot

@hook.command
def imitate(bot_input, bot_output):
    message = get_markov().imitate(bot_input, bot_output)
    if message:
        bot_output.say(message)

@hook.command
def cite(bot_input, bot_output):
    message = get_markov().cite(bot_input, bot_output)
    if message:
        bot_output.say(message)

@hook.regex('.*', run_always=True)
def markov_master(bot_input, bot_output):
    marvin_kov = get_markov()
    message = marvin_kov.log(bot_input, bot_output)
    if message:
        bot_output.say(message)