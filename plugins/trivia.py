from util import hook, textutils
import random

first_time = True

science = {
    "What is September's birthstone": "sapphire",
    "What is the minimum number of bars on an abacus": "9",
    "How many carats is pure gold": "24",
    "What is January's birthstone": "garnet",
    "Approximately how many miles are there in a nautical mile": "1.15",
    "What is a group of lions called": "pride",
    "How many canine teeth are there in a normal set of human teeth": "4",
    "In what decade was the very first test-tube baby born": "1978",
    "What period saw the first dinosaurs": "triassic",
    "How many chromosomes does a cow have": "60",
    "What percentage of air is composed of oxygen": "21",
    "A male swan is called a what": "cob",
    "What fiber-producing plant is attacked by the boll weevil": "cotton",
    "What constellation is represented by the whale": "cetus",
    "What color is a Great Egret": "white",
    "What method of food preservation was invented for the British Navy in 1813": "canning",
    "What astrological chart takes its name from a Greek word meaning 'circle of little animals'": "zodiac"
}


current_trivia = {}

@hook.command
def trivia(bot_input, bot_output):
    question = random.choice(science.keys())
    current_trivia['question'] = question
    current_trivia['answer'] = science[question]
    bot_output.say('{0}?'.format(question))

@hook.command
def answer(bot_input, bot_output):
    if bot_input.input_string:
        check_trivia(bot_input, bot_output)
    else:
        bot_output.say("Okay, {0}.  The answer to {1} is {2}".format(bot_input.nick, current_trivia['question'], current_trivia['answer']))
        current_trivia['question'] = ''


def check_trivia(bot_input, bot_output):
    if current_trivia['question']:
        guess = textutils.sanitize_message(bot_input.message)
        if guess in current_trivia['answer']:
            bot_output.say("That's correct, {0}.  The answer to {1} is {2}".format(bot_input.nick, current_trivia['question'], current_trivia['answer']))
            current_trivia['question'] = ''
        else:
            bot_output.say("WRONG!")
