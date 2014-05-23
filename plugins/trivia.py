from util import hook, textutils, storage
import random
import os
import json

current_trivia = {}
user_points = {}
list_name = "trivia:points"
question_list = {}

def new_question(category=None):
    category_to_pick = category or random.choice(question_list.keys())
    question = random.choice(question_list[category_to_pick].keys())
    current_trivia['question'] = question
    current_trivia['category'] = category_to_pick
    current_trivia['answer'] = question_list[category_to_pick][question]
    current_trivia['guess'] = 0
    current_trivia['multiplier'] = 1

def compare_values(guess, answer):
    if textutils.is_int(answer) and textutils.is_int(guess):
        return int(answer) == int(guess)
    elif type(answer) is list:
        return guess in answer
    else:
        return textutils.equal_letters(guess, answer)

@hook.command
def trivia(bot_input, bot_output):
    if "reset" in bot_input.input_string:
        storage.set_hash_value(list_name, bot_input.nick, 0)
        user_points[bot_input.nick] = 0
        bot_output.say("{0}'s score is now 0".format(bot_input.nick))
    elif "score" in bot_input.input_string:
        get_points(bot_input, bot_output)
    elif "categories" in bot_input.input_string:
        bot_output.say(', '.join(question_list.keys()))
    else:
        if not current_trivia.has_key('question'):
            if bot_input.input_string in question_list:
                new_question(bot_input.input_string)
            else:
                new_question()
        else:
            bot_output.say("Use '.answer' to get the answer and a new question\nUse .trivia categories to see all categories\nUse .trivia <category name> to get questions from a certain category\nUse .trivia points to see current score\nUse birth control to prevent more wrong answers\n\nCurrent question:")
        bot_output.say('Category: %(category)s\n%(question)s?' % current_trivia)


@hook.command
def answer(bot_input, bot_output):
    if bot_input.input_string:
        check_trivia(bot_input, bot_output)
    else:
        bot_output.say("Okay, {0}.  The answer to {1} is {2}".format(bot_input.nick, current_trivia['question'], current_trivia['answer']))
        new_question()
        if random.choice(range(20)) == 1:
            bot_output.say("NOISE NOISE NOISE\nDaily Double!\nThe next correct answer is worth 10 times the normal amount!\nThat's binary double, in case you're wondering.\nNOISE NOISE NOISE")
            current_trivia['multiplier'] = 10
        bot_output.say('Category: %(category)s\n%(question)s?' % current_trivia)

def check_trivia(bot_input, bot_output):
    if current_trivia['question']:
        guess = textutils.sanitize_message(bot_input.input_string)
        current_answer = current_trivia['answer']
        if compare_values(guess, current_answer):
            bot_output.say("That's correct, {0}.  The answer to {1} is {2}".format(bot_input.nick, current_trivia['question'], current_trivia['answer']))
            if current_trivia['guess'] == 0:
                bot_output.say('2 points for guessing on the first try.')
                add_point(bot_input.nick, 2)
            else:
                bot_output.say('1 point.')
                add_point(bot_input.nick, 1)
            get_points(bot_input, bot_output)
            new_question()
            bot_output.say('Next question\nCategory: %(category)s\n%(question)s?' % current_trivia)
        else:
            current_trivia['guess'] += 1
            bot_output.say("WRONG {0}! Minus 1 point!".format(bot_input.nick).upper())
            add_point(bot_input.nick, -1)

def add_point(nick, points):
    current_score = int(storage.get_hash_value(list_name, nick) or 0)
    if points > 0:
        points = points * current_trivia['multiplier']
    user_points[nick] = current_score + points
    storage.set_hash_value(list_name, nick, user_points[nick])

def get_points(bot_input, bot_output):
    messages = []
    for user, points in user_points.iteritems():
        messages.append("%s has %d" % (user,points))
    bot_output.say("Current Score: ")
    bot_output.say("\n".join(messages))


def load_questions(category, file):
    questions = open(file, 'r')
    question_list[category] = json.load(questions)


files = os.listdir('trivia')
for file_name in files:
    load_questions(file_name, 'trivia/' + file_name)
