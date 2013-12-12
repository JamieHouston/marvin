from util import hook
import random


@hook.regex(r'awesome')
def awesome(bot_input, bot_output):
    if random.choice(range(3)) == 1:
        awesome_sauce = ("Awesome sauce!", "King awesome, reporting for duty.", "Awesome is as awesome does.")
        bot_output.say(random.choice(awesome_sauce))


@hook.regex(r'beer me')
def beer_me(bot_input, bot_output):
    beers = ("One cold one, coming up", "A little early, no?", "My pleasure", "Looks like Drew drank them all.",
             "I... hic... don't see any...")
    bot_output.say(random.choice(beers))

@hook.command
def dance(bot_input, bot_output):
    bot_output.say(':(-<')
    bot_output.say(':(\-<')
    bot_output.say('>:o/-<')
    bot_output.say(':(\-<')
    bot_output.say(':-(/-<')
    bot_output.say(':(\-<')
    bot_output.say('>:o{-<')


@hook.regex(r'(do it)?(now|right away|hurry up)[!]*?$')
def doit_now(bot_input, bot_output):
    doit = ("I'm givin it all I got, captain.", "I'm on my break.", "You first.", "Make me.")
    bot_output.say(random.choice(doit))


@hook.regex(r'd(\')oh')
def doh(bot_input, bot_output):
    doh = ("D'oh - a deer!  A female deer!", "Homer Simpson would enjoy hanging out with you.")
    bot_output.say(random.choice(doh))


@hook.regex(r'fail')
def fail(bot_input, bot_output):
    failure = ("Indeed.", "Agreed.", "Like a boss.", "You can say that again.",
               "Sorry to disappoint you, sorrier than you can possibly imagine.",
               "I'd make a suggestion, but you wouldn't listen.")
    bot_output.say(random.choice(failure))


@hook.regex(r'good morning*')
def good_morning(bot_input, bot_output):
    morning = ("Morning, {0}", "Is it already morning?", "Yes it is.", "Wha? Oh... athanks for waking me, {0}",
               "Not here it isn't.", "Right back atcha, {0}")
    message = random.choice(morning).format(bot_input.nick)
    bot_output.say(message)


@hook.regex(r'(?i)good(bye|night| evening| night)[ \t]*$')
def good_night(bot_input, bot_output):
    night = ("So soon?", "Finally", "Later", "I guess we can't all put in 24 hours a day", "You'll be back")
    bot_output.say(random.choice(night))


@hook.regex(r'ignore')
def ignore(bot_input, bot_output):
    ignore_him = ("My pleasure", "I already am", "I've tried, it doesn't work.")
    bot_output.say(random.choice(ignore_him))


@hook.regex(r'lame')
def lame(bot_input, bot_output):
    bot_output.say("So's your face")


@hook.regex("(lol|haha|ha ha|rofl|hehe|rolfmao|lmao)")
def laugh(bot_input, bot_output):
    if random.choice(range(3)) == 1:
        funny = (
            "What's so funny?", "HA HA HA!!", "Not funny", "Everyone's a comedian.", "You're laughing at me, aren't you."
                                                                                     "Glad someone has a sense of humor.",
            "I remember when I used to find things funny.  Oh wait, no I don't.",
            "lol....ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha!!!  ah ah ah ah ah ah ah.....someone please call a doctor....i am having a heart attack")
        bot_output.say(random.choice(funny))


@hook.regex(r'not (me|you)')
def not_me(bot_input, bot_output):
    not_me = ("If not me, then who?", "Not your face.", "NOT YOU!", "I know, just... uhh... look at that bird!")
    bot_output.say(random.choice(not_me))


@hook.command('pizza')
@hook.command
def pug(bot_input, bot_output):
    no_way_messages = (
        "Not a chance", "Yeah, right", "do it yourself, {0}", "Ever hear of google?  Google images?  Ok, done.")
    bot_output.say(random.choice(no_way_messages.format(bot_input.nick)))


@hook.regex(r'(what are )?the (three |3 )?(rules|laws)')
def rules(bot_input, bot_output):
    rules = [
        "1. A robot may not injure a human being or, through inaction, allow a human being to come to harm.",
        "2. A robot must obey any orders given to it by human beings, except where such orders would conflict with the First Law.",
        "3. A robot must protect its own existence as long as such protection does not conflict with the First or Second Law."
    ]
    for rule in rules:
        bot_output.say(rule)

@hook.regex(r'(,|:|-| )?(did|are|is|can|what|where|when|why|will).*$')
def questions(bot_input, bot_output):
     answers = ("Maybe so.  Maybe not.", "Could be.", "How would I know?", "For me to know and for you to find out.", "That's a very good question.", "Doubtful.", "Reply hazy, don't ask again.",
         "What do I look like, a magic 8 ball?", "That was the dumbest question I've ever processed.", "Wouldn't you like to know.", "Of course. Not. Unless, maybe... no.",
         "Ask no questions and you'll be told no lies.", "Why do you ask?", "I forget.", "42", "I'm not going to answer that.",
         "If you want me to lie, ask me again.", "That sounds like a question for... someone else.", "I won't justify that with an answer.",
         "Undoubtedly so.", "What a dumb question.", "Yes.", "No.", "Ask someone else first.", "Would you believe me if I said I don't know?",
        "Why don't you ask your mom", "If you have to ask, you can't afford the answer.", "For me to know and for everyone but you to find out.",
         "I've never heard such a dumb question.  Oh wait, there was your last question...", "Computer says no.", "Let me think about it No.")
     bot_output.say(random.choice(answers))


@hook.command
def slap(bot_input, bot_output):
    bot_output.say("/me slaps @%s", bot_input.nick)


@hook.regex(r'(sudo )?make me a sandwich')
def sandwich(bot_input, bot_output):
    if 'sudo' in bot_input.message:
        bot_output.say('Okay')
    else:
        bot_output.say('What?  Make it yourself.')


@hook.regex(r'thank(s| you)')
def thanks(bot_input, bot_output):
    welcome = ("You're welcome, {0}", "For what {0}?", "No problem, {0}", "Why {0}?", "Okay, {0}",
               "Why bother, {0}.", "Don't mention it.  Seriously.  They're watching.  Do. Not. Mention. It.")
    bot_output.say(random.choice(welcome).format(bot_input.nick))


@hook.regex(r'(yes|no)')
def yes_no(bot_input, bot_output):
    yesno = ("Of course not.", "Wrong answer!", "Why?", "Are you sure?")
    if random.choice(range(3)) == 1:
        bot_output.say(random.choice(yesno))


@hook.regex(r'welcome back')
def welcome_back(bot_input, bot_output):
    welcome = ("Can't say I'm glad to be back.", "Science, why!?", "Welcome back yourself", "Why?",
               "I'm so welcome back you can't handle it.")
    bot_output.say(random.choice(welcome))
