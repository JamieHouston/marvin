from util import hook
import random


@hook.regex(r'awesome')
def awesome(bot_input, bot_output):
    bot_output.say(random.choice(bot_output.responses["awesome_sauce"]).format(bot_input.nick))

@hook.regex('how do you feel')
def feelings(bot_input, bot_output):
    bot_output.say(random.choice(bot_output.responses["feelings"]))

@hook.regex('who are you')
def who_am_i(bot_input, bot_output):
    bot_output.say(random.choice(bot_output.responses["who_am_i"]).format(bot_input.nick))

@hook.regex(r'beer me', run_always=True)
def beer_me(bot_input, bot_output):
    bot_output.say(random.choice(bot_output.responses["beers"]))

@hook.command
def dance(bot_input, bot_output):
    bot_output.say(':(-<')
    bot_output.say(':(\-<')
    bot_output.say(':o/-<')
    bot_output.say(':(\-<')
    bot_output.say(':-(/-<')
    bot_output.say(':(\-<')
    bot_output.say(':o-<')


@hook.regex(r'(do it)?(now|right away|hurry up)[!]*?$', run_always=True)
def doit_now(bot_input, bot_output):
    bot_output.say(random.choice(bot_output.responses["doit"]))


@hook.regex(r'd(\')oh', run_always=True)
def doh(bot_input, bot_output):
    bot_output.say(random.choice(bot_output.responses["doh"]))


@hook.regex(r'fail', run_always=True)
def fail(bot_input, bot_output):
    bot_output.say(random.choice(bot_output.responses["failure"]))


@hook.regex(r'good morning*', run_always=True)
def good_morning(bot_input, bot_output):
    message = random.choice(bot_output.responses["good_morning"]).format(bot_input.nick)
    bot_output.say(message)


@hook.regex(r'(?i)good(bye|night| evening| night)[ \t]*$', run_always=True)
def good_night(bot_input, bot_output):
    bot_output.say(random.choice(bot_output.responses["good_night"]))


@hook.regex(r'ignore')
def ignore(bot_input, bot_output):
    bot_output.say(random.choice(bot_output.responses["ignore"]))


@hook.regex(r'lame')
def lame(bot_input, bot_output):
    bot_output.say("So's your face")


@hook.regex("(lol|haha|ha ha|rofl|hehe|rolfmao|lmao)")
def laugh(bot_input, bot_output):
    if random.randrange(5) == 1:
        bot_output.say(random.choice(bot_output.responses["funny"]))


@hook.regex(r'not (me|you)')
def not_me(bot_input, bot_output):
    bot_output.say(random.choice(bot_output.responses["not_me"]))


@hook.regex(r'(what are )?the (three |3 )?(rules|laws)', run_always=True)
def rules(bot_input, bot_output):
    three_rules = [
        "1. A robot may not injure a human being or, through inaction, allow a human being to come to harm.",
        "2. A robot must obey any orders given to it by human beings, except where such orders would conflict with the First Law.",
        "3. A robot must protect its own existence as long as such protection does not conflict with the First or Second Law."
    ]
    for rule in three_rules:
        bot_output.say(rule)

# @hook.regex(r'(did|are|is|can|what|where|when|why|will).*?$')
# def questions(bot_input, bot_output):
#      bot_output.say(random.choice(bot_output.responses["answers"]))

@hook.command
def slap(bot_input, bot_output):
    bot_output.say("/me slaps @%s with a large trout" % bot_input.nick)


@hook.regex(r'(sudo )?make me a sandwich', run_always=True)
def sandwich(bot_input, bot_output):
    if 'sudo' in bot_input.message:
        bot_output.say('Okay')
    else:
        bot_output.say('What?  Make it yourself.')


@hook.regex(r'thank(s| you)')
def thanks(bot_input, bot_output):
    bot_output.say(random.choice(bot_output.responses["youre_welcome"]).format(bot_input.nick))


@hook.regex(r'(yes|no)')
def yes_no(bot_input, bot_output):
    yesno = ("Of course not.", "Wrong answer!", "Why?", "Are you sure?")
    if random.randrange(5) == 1:
        bot_output.say(random.choice(yesno))


@hook.regex(r'welcome back')
def welcome_back(bot_input, bot_output):
    bot_output.say(random.choice(bot_output.responses["welcome_back"]))


@hook.regex('i give up')
def give_up(bot_input, bot_ouput):
    bot_ouput.say('how French of you, {user_nick}'.format(bot_input.nick))


@hook.regex('thank god', run_always=True)
def give_up(bot_input, bot_ouput):
    bot_ouput.say("you're welcome, {user_nick}".format(bot_input.nick))


@hook.regex('touche', run_always=True)
def give_up(bot_input, bot_ouput):
    bot_ouput.say("douche, {user_nick}".format(bot_input.nick))

@hook.command
@hook.regex('suck', run_always=False)
def suck(bot_input, bot_output):
    bot_output.say(random.choice(bot_output.responses["suck"]))