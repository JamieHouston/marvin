from util import hook, textutils
import random

first_time = True

science = {
    "What is September's birthstone": "sapphire",
    "What is the minimum number of bars on an abacus": ["9", "nine"],
    "How many carats is pure gold": "24",
    "What is January's birthstone": "garnet",
    "Approximately how many miles are there in a nautical mile": "1.15",
    "What is a group of lions called": "pride"
}


current_trivia = {}

@hook.command
def trivia(bot_input, bot_output):
    #if not current_question:
    question = random.choice(science.keys())
    current_trivia['question'] = question
    current_trivia['answer'] = science[question]
    bot_output.say('{0}?'.format(question))

@hook.command
def answer(bot_input, bot_output):
    bot_output.say("Okay, {0}.  The answer to {1} is {2}".format(bot_input.nick, current_trivia['question'], current_trivia['answer']))
    current_trivia['question'] = ''


@hook.regex(r'.*', run_always=True)
def check_trivia(bot_input, bot_output):
    if current_trivia['question']:
        guess = textutils.sanitize_message(bot_input.message)
        if guess in current_trivia['answer']:
            bot_output.say("That's correct, {0}.  The answer to {1} is {2}".format(bot_input.nick, current_trivia['question'], current_trivia['answer']))
            current_trivia['question'] = ''
