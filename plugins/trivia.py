from util import hook, textutils, storage, web
import random
import os
import json
import re

current_trivia = {}
user_points = {}
list_name = "trivia:points"
question_list = {}

def new_question(category=None):
    url = 'https://privnio-trivia.p.mashape.com/exec?category=' + bot_input.input_string + '&method=getQuestions&v=1'
    headers={
        "X-Mashape-Key": "LM6TApHaSPmshsDRI2S9h2W5eYvNp1Iin3Vjsn2ZncHbuAbsHt",
        "Accept": "application/json"
    }

    result = web.get_json_with_headers(url, headers)
    if not result or not result["success"]:
        bot_output.say("Couldn't get the questions.  Maybe you're over your quota?")
        return


    questionPage = web.get_raw('http://www.quinterest.org/php/studyresults.php?amount=1&categ=All&difficulty=MS&tournamentyear=All')

    current_trivia['question'] = re.search("<p><em>Question:</em>(.*)</p>").groups()[0]
    current_trivia['category'] = re.search("(<b>.*</b>){4}<b>(.*)</b><p>").groups()[1]
    current_trivia['answer'] = re.search("<em><strong>Answer:</strong></em>(.*)</div>").groups()[0]
    current_trivia['guess'] = 0
    current_trivia['multiplier'] = 1

def compare_values(guess, answer_given):
    if textutils.is_int(answer_given) and textutils.is_int(guess):
        return int(answer_given) == int(guess)
    elif type(answer_given) is list:
        return guess in answer_given
    else:
        return textutils.equal_letters(guess, answer_given)

@hook.command
def trivia(bot_input, bot_output):
    if "reset" in bot_input.input_string:
        storage.set_hash_value(list_name, bot_input.nick, 0)
        user_points[bot_input.nick] = 0
        bot_output.say("{0}'s score is now 0".format(bot_input.nick))
    elif "reload" in bot_input.input_string:
        load_questions()
    elif "score" in bot_input.input_string:
        get_points(bot_input, bot_output)
    elif "categories" in bot_input.input_string:
        bot_output.say(', '.join(list(question_list.keys())))
    elif bot_input.input_string in question_list:
        new_question(bot_input.input_string)
    else:
        if 'question' not in current_trivia:
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
        if random.choice(list(range(20))) == 1:
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
    for user, points in user_points.items():
        messages.append("%s has %d" % (user,points))
    bot_output.say("Current Score: ")
    bot_output.say("\n".join(messages))


def load_questions():
    files = os.listdir('trivia')
    for file_name in files:
        with open('trivia/' + file_name, 'r', encoding="utf-8") as questions:
            question_list[file_name] = json.load(questions)


load_questions()
