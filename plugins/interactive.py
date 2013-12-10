from util import hook
import random

@hook.regex(r'(?i)thank(s| you)')
def thanks(bot_input, bot_output):
    welcome = ("You're welcome, {0}", "For what {0}?", "No problem, {0}", "Why {0}?", "Okay, {0}",
        "Why bother, {0}.")
    bot_output.say(random.choice(welcome).format(bot_input.nick))


@hook.regex(r'(yes|no)')
def yes_no(bot_input, bot_output):
    yesno = ("Of course not.", "Wrong answer!", "Why?", "Are you sure?")
    if random.choice(range(3)) == 1:
        bot_output.say(random.choice(yesno))


@hook.regex(r'awesome')
def awesome(bot_input, bot_output):
    if random.choice(range(3)) == 1:
        awesome_sauce = ("Awesome sauce!", "King awesome, reporting for duty.", "Awesome is as awesome does.")
        bot_output.say(random.choice(awesome_sauce))


@hook.regex(r'fail')
def fail(bot_input, bot_output):
    failure = ("Indeed.", "Agreed.", "Like a boss.", "You can say that again.", "Sorry to disappoint you, sorrier than you can possibly imagine.", "I'd make a suggestion, but you wouldn't listen.")
    bot_output.say(random.choice(failure))


@hook.regex("(lol|haha|ha ha|rofl|hehe|rolfmao|lmao)")
def laugh(bot_input, bot_output):
    if random.choice(range(3)) == 1:
        funny = ("What's so funny?", "HA HA HA!!", "Not funny", "Everyone's a comedian.", "You're laughing at me, aren't you."
        "Glad someone has a sense of humor.", "I remember when I used to find things funny.  Oh wait, no I don't.", "lol....ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha!!!  ah ah ah ah ah ah ah.....someone please call a doctor....i am having a heart attack")
        bot_output.say(random.choice(funny))


@hook.regex(r'not you')
def not_me(bot_input, bot_output):
    not_me = ("If not me, then who?", "Not your face.", "NOT YOU!", "I know, just... uhh... look at that bird!")
    bot_output.say(random.choice(not_me))