from util import hook, textutils
import random

words = {
    'd': ['darpa', 'dragon', 'deadly', 'dumb', 'deranged', 'default', 'department', 'decidedly', 'decadent', 'dancing', 'denied', 'deathly', 'death', 'drunk', 'dastardly', 'dreaded', 'devilish', 'demonic'],
    'l': ['loser', 'lasting', 'last', 'lemony', 'lemon', 'landlocked', 'list', 'loving', 'lover', 'linguistic', 'lard', 'lamp', 'listed', 'laughable', 'luxerious', 'lusty', 'ladies', 'long', 'laxative'],
    'r': ['reserved', 'reservation', 'renowned', 'religous', 'risky', 'risk-adverse', 'readers', 'rated', 'room', 'rewards', 'relaxed', 'relaxing', 'remembered', 'rough', 'rental', 'retail'],
    't': ['tough', 'two', 'twisted', 'tentative', 'tasty', 'tri', 'triangulated', 'trippy', 'tools', 'tangible', 'tenacious', 'tangled', 'tenfold', 'terrible', 'talkative', 'trusted', 'treehugging']
}

@hook.command
def acronym(bot_input, bot_output):
    result = []
    letters = textutils.strip(bot_input.input_string).split('')
    for letter in letters:
        result.append(random.choice(words[letter]))
    bot_output.say(result.join(' '))