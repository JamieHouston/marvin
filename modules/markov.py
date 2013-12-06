#!/usr/bin/env python
"""
markov.py - Markov List
Attempts to put together a list of what people say and say it back in the correct syntax
"""

import os,sys
import pickle
import random
import re
from util import logger

class Markov(object):
    """
    Hacking on a markov chain bot - based on:
    http://code.activestate.com/recipes/194364-the-markov-chain-algorithm/
    http://github.com/ericflo/yourmomdotcom
    """
    messages_to_generate = 5
    chattiness = .01
    max_words = 15
    chain_length = 2
    stop_word = '\n'
    filename = 'markov.db'
    last = None
    activities = 0

    def __init__(self):
        logger.log("loading new Markov bot")
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
            logger.log("Not enough words to imitate.  Found %d words" % person_words)
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

    def knowledge(self, flowbot, input):
        #flowbot.say(",".join(self.word_table.get(input.nick, {})))
        words = self.word_table.get(input.nick)
        if words and len(words):
            flowbot.say(",".join(words.items()))
        else:
            flowbot.say("Not gonna happen.")

    def imitate(self, flowbot, input):
        #print >> sys.stderr, "Imitating: {0}".format(input.group(2))
        #person = input.group(2).strip()[:10]
        person = input.nick
        if person != flowbot.nick:
            return self.generate_message(person)

    def cite(self, flowbot, input):
        if self.last:
            return self.last

    def sanitize_message(self, message):
        """Convert to lower-case and strip out all quotation marks"""
        return re.sub('[\"\']', '', message.lower())

    def is_ping(self, message, flowbot):
        return re.match('^%s[:,\s]' % flowbot.nick, message) is not None

    def fix_ping(self, message, flowbot):
        return re.sub('^%s[:,\s]\s*' % flowbot.nick, '', message)

    def log(self, flowbot, input):
        #pdb.set_trace()
        #print >> sys.stderr, "Logging from {0} message: {1}".format(input.nick, input.group(0))
        sender = input.nick[:10]
        message = input.content
        self.word_table.setdefault(sender, {})

        if message.startswith('/') or message.startswith('.'):
            return

        try:
            say_something = self.is_ping(message, flowbot) or sender != flowbot.nick and random.random() < self.chattiness
            #print >> sys.stderr, "Say something is: {0}".format(say_something)
        except AttributeError:
            say_something = False
        messages = []
        seed_key = None

        if self.is_ping(message, flowbot):
            message = self.fix_ping(message, flowbot)

        for words in self.split_message(self.sanitize_message(message)):
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

        if len(messages):
            self.last, message = random.choice(messages)
            if self._should_update():
                self._save_data()
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

def markov_imitate(flowbot, input):
    logger.log("trying to imitate")
    if ("debug" in input.content):
        message = get_markov().knowledge(flowbot, input)
    else:
        message = get_markov().imitate(flowbot, input)
    if message:
        logger.log("found message %s" % message)
        flowbot.say(message)
    else:
        flowbot.say("No way I'm imitating you.  This time.")
        logger.log("No message returned")
#markov_imitate.commands = ['imitate']

def markov_cite(flowbot, input):
    message = get_markov().cite(flowbot, input)
    if message:
        flowbot.say(message)
#markov_cite.commands = ['cite']

def markov_master(flowbot, input):
    logger.log("logging markov message %s" % input.content)
    marvin_kov = get_markov()
    message = marvin_kov.log(flowbot, input)
    if message:
        flowbot.say(message)

#markov_master.rule = r'(.*)'


if __name__ == '__main__':
    print __doc__.strip()
