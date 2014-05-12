from util import hook, textutils, storage
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
    "What astrological chart takes its name from a Greek word meaning 'circle of little animals'": "zodiac",
    "What is the acronym for Thomas A. Swift's Electric Rifle": "taser",
    "Where in your body would you find your hippocampus": "brain",
    "What is the only mammal with four knees": "elephant",
    "What is added to bread to make it swell": "yeast",
    "What fruit comes in Key and Kaffir variety": "lime",
    "In what century did the Dodo bird become extinct": "17",
    "Hg is the symbol for what element": "mercury",
    "How many land miles are there in a league": "3",
    "How many kilograms are there in a short ton": "907",
    "Which body joint includes the patella": "knee",
    "What name is given to male rhinoceroses": "bull",
    "What fruit comes in Hass and Florida variety": "avocado",
    "In what country would you most likely encounter a Tasmanian devil": "australia",
    "What does an archer keep his arrows in": "quiver",
    "What does a phonophobe fear": "noise",
    "In which ocean is the area known as Polynesia located": "pacific",
    "Who was the Roman demigod best known for his strength": "hercules",
    "How many points is the outer white ring of an Olympic archery target worth": "1",
    "What number is indicated by the Roman numeral 'D'": "500",
    "What country is home to the original Highland Games": "scotland",
    "Which continent has never hosted the Olympics": "antartica",
    "What is the dot in the 'i' called": "tittle",
    "Which US state is nicknamed the 'Old Dominion' state": "virginia"
}

current_trivia = {}
user_points = {}
list_name = "trivia:points"

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
        guess = textutils.sanitize_message(bot_input.input_string)
        if guess in current_trivia['answer']:
            add_point(bot_input.nick)
            bot_output.say("That's correct, {0}.  The answer to {1} is {2}".format(bot_input.nick, current_trivia['question'], current_trivia['answer']))
            current_trivia['question'] = ''
        else:
            bot_output.say("WRONG!")

def add_point(nick):
    points = storage.get_hash_value(list_name, nick) or 0
    user_points[nick] = points + 1
    storage.set_hash_value(list_name, nick, user_points[nick])

@hook.regex(r'trivia score', run_always=True)
def get_points(bot_input, bot_output):
    messages = []
    for user, points in user_points.iteritems():
        messages.append("%s has %d" % (user,points))
    bot_output.say("Current Score: ")
    bot_output.say(", ".join(messages))

