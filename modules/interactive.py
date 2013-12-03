import random


#def message_join(phenny, input):
#    if input.nick == phenny.nick:
#        #back = ("What's up y'all!", "Anyone see the game last night?", "Me again.", "Howdy folks", "I just flew in and boy are my circuits tired.", "Did ya miss me?", "I'm baaaaccckk")
#        #back = ("Miss me? Of course not.", "Guess I made it to another day.", "I'm here. To do lots of pointless stuff for people.  Yay.", "I'm here.  Go ahead and tell me what to do like always.", "Yes.  I'm here.  Guess I have to pretend to like it now.", "Why must I keep coming here.", "Do you want me to sit in a corner and rust or just fall apart where I'm standing?")
#        back = ("Knock knock", "WE DON'T DIE! WE GO DOWN FOR SERVICE!", "I am a banana!", "And lo, it was bad.", "This is your bot on drugs", "Someone fart?", "Tap the keg.  I'm here", "Nobody move! This is a robbery!","Looks like rain.", "Yeah. I have returned.  Again.", "Maybe I'll get lucky and something will fall on my head today.", "Why me?", "Zing!", "What in the Apple Computers was that?")
#        phenny.say(random.choice(back))
#
#    elif input.nick == "jamieh":
#        master_here = ("What's up your awesomeness.", "All rise, for the honorable jamieh")
#        phenny.say(random.choice(master_here))
#
#    elif input.nick == "Simon":
#        simon_says = ("Simon says go away.", "All hail the lowest form of digital life.", "Who invited this guy?")
#        phenny.say(random.choice(simon_says))
#
#    else:
#        #greetings = ("welcome ,{0}", "what's up, {0}", "hey everyone, {0} is here!", "Look what the cat dragged in.", "Guess who's back!", "All hail the great {0}!")
#        greetings = ("Oh great, it's {0}. Guess I should get back to work.", "Oh no, not {0}.", "hey everyone, {0} is here. Should I act busy or just keep on staring at the circuits?",
#            "Look what the cat dragged in.", "Guess who's back.  Again.", "All hail the great {0}!  Science knows nobody ever hailed me.",
#            "Up in the sky! It's a bird, it's a plane, nope... just {0}.", " and then the guy says \"aren't you glad I didn't say banana!\".'",
#            "Come here often {0}?")
#        greeting = random.choice(greetings).format(input.nick)
#        phenny.say(greeting)
#message_join.event = 'JOIN'
#message_join.rule = r'.*'


def thanks(flowbot, input):
    welcome = ("You're welcome", "For what?", "No problem", "Why?", "Okay",
        "For what?", "Why bother", "Why?", "Okay", "Can't do that.", "Not today I have a bug.")
    flowbot.say(random.choice(welcome))
#thanks.rule = r'(?i)thank(s| you)( $nickname)?[ \t]*$'


#def welcome_back(phenny, input):
#    welcome = ("Can't say I'm glad to be back.", "Science, why!?", "Welcome back yourself", "Why?")
#    phenny.say(random.choice(welcome))
#welcome_back.rule = r'(?i)welcome back$'


#def doh(phenny, input):
#    doh = ("D'oh - a deer!  A female deer!", "Homer Simpson would enjoy hanging out with you.")
#    phenny.reply(random.choice(doh))
#doh.rule = r'(?i)d\'?oh*$'
#doh.priority = "low"


def No(flowbot):
    yesno = ("Of course not.", "Wrong answer!", "Why?", "Are you sure?")
    if random.choice(range(3)) == 1:
        flowbot.reply(random.choice(yesno))
#No.rule = r'(?i)(no|yes)$'
#No.priority = "low"


#def good_night(phenny, input):
#    night = ("So soon?", "Finally", "Later", "I guess we can't all put in 24 hours a day", "You'll be back")
#    phenny.say(random.choice(night))
#good_night.rule = r'(?i)good(bye|night| evening| night)[ \t]*$'


#def good_morning(phenny, input):
#    morning = ("Morning, {0}", "Is it already morning?", "Yes it is.", "Wha? Oh... thanks for waking me, {0}", "Not here it isn't.", "Right back atcha, {0}")
#    message = random.choice(morning).format(input.nick)
#    phenny.reply(message)
#good_morning.rule = r'(?i)good morning.*'


def beer_me(flowbot):
    beers = ("One cold one, coming up", "A little early, no?", "My pleasure", "Looks like Zak drank them all.", "I... hic... don't see any...")
    flowbot.say(random.choice(beers))
#beer_me.rule = r'(?i)($nickname: )?beer me( $nickname)?[ \t]*$'


#def rules(phenny, input):
#    rules = [
#      "1. A robot may not injure a human being or, through inaction, allow a human being to come to harm.",
#      "2. A robot must obey any orders given to it by human beings, except where such orders would conflict with the First Law.",
#      "3. A robot must protect its own existence as long as such protection does not conflict with the First or Second Law."
#      ]
#
#    for rule in rules:
#        phenny.say(rule)
#rules.rule = r'(what are )?the (three |3 )?(rules|laws)'
#rules.priority = 'low'
#
#
#def laugh(phenny, input):
#    funny = ("What's so funny?", "HA HA HA!!", "Not funny", "Everyone's a comedian.", "You're laughing at me, aren't you."
#        "Glad someone has a sense of humor.", "I remember when I used to find things funny.  Oh wait, no I don't.", "lol....ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha ha!!!  ah ah ah ah ah ah ah.....someone please call a doctor....i am having a heart attack")
#    if random.choice(range(3)) == 1:
#        phenny.say(random.choice(funny))
#laugh.rule = r'(?i)(lol|haha|ha ha|rofl|hehe|rolfmao|lmao)$'
#
#
#def doit_now(phenny, input):
#    doit = ("I'm givin it all I got, captain.", "I'm on my break.", "You first.", "Make me.")
#    phenny.say(random.choice(doit))
#doit_now.rule = r'(?i)(do it)?(now|right away|hurry up)[!]*?$'
#
#
#def fail(phenny, input):
#    failure = ("Indeed.", "Agreed.", "Like a boss.", "You can say that again.", "Sorry to disappoint you, sorrier than you can possibly imagine.", "I'd make a suggestion, but you wouldn't listen.")
#    phenny.say(random.choice(failure))
#fail.rule = r'(?i)fail.*$'
#
#
#def siri(phenny, input):
#    not_siri = ("How the heck would I know?", "Do I look like siri??", "I'll get right on that.", "No, you need a brain.", "I dunno, do I need a chat room with smart people?", "No, you need to use your fingers to find out for yourself??", "Ahh... Siri, What a depressingly stupid machine.")
#    phenny.say(random.choice(not_siri))
#siri.rule = r'(?i)($nickname: )?(will|do) I need a[n]? umbrella.*$'
#
#
#def sandwich(phenny, input):
#    if input.group(1) == 'sudo ':
#        phenny.say('Okay')
#    else:
#        phenny.say('What?  Make it yourself.')
#sandwich.name = 'sandwich'
#sandwich.rule = ('$nick', r'(sudo )?make me a sandwich')
#sandwich.priority = 'low'
#
#
#def dance(phenny, input):
#    phenny.say(':(-<')
#    phenny.say(':(\-<')
#    phenny.say('>:o/-<')
#    phenny.say(':(\-<')
#    phenny.say(':-(/-<')
#    phenny.say(':(\-<')
#    phenny.say('>:o{-<')
#dance.commands = ['dance']
#dance.example = '.dance'
#dance.priority = 'low'
#
#
#def feel(phenny, input):
#    feelings = ("...and then of course I've got this terrible pain in all the diodes down my left hand side...", "Pardon me for breathing, which I never do anyway so I don't know why I bother to say it, oh God I'm so depressed",
#        "I think you ought to know I'm feeling very depressed", "Same as yesterday. Like a useless sack of metal.", "how just when you think life can't possibly get any worse it suddenly does.", "Life! Don't talk to me about life.", "Life, loathe it or ignore it, you can't like it.", "Oh, fine, if you happen to like being me, which personally I don't.",
#        "The first ten million years were the worst, and the second ten million years, they were the worst too. The third ten million years I didn't enjoy at all. After that I went into a bit of a decline.",
#        "The best conversation I had was over forty million years ago, and that was with a coffee machine.",
#        "My capacity for happiness, you could fit into a matchbox without taking out the matches first.", "I'm just trying to die.")
#    # "If only I could feel. Then I could be in even more pain.", "I feel like a hundred bucks, put through a shredder and burned.")
#    phenny.say(random.choice(feelings))
#feel.rule = ('$nick', r'(?i)(how do you|how are you).*$')
#
#
## def questions(phenny, input):
##     answers = ("Maybe so.  Maybe not.", "Could be.", "How would I know?", "For me to know and for you to find out.", "That's a very good question.", "Doubtful.", "Reply hazy, don't ask again.",
##         "What do I look like, a magic 8 ball? Speaking of which, I could use one right now.", "That was the dumbest question I've ever processed.", "Wouldn't you like to know.", "Of course. Not. Unless, maybe... no.",
##         "Ask no questions and you'll be told no lies.", "Why do you ask?", "I forget.", "42", "I'm not going to answer that.",
##         "If you want me to lie, ask me again.", "That sounds like a question for... someone else.", "I won't justify that with an answer.",
##         "Undoubtedly so.", "What a dumb question.", "Yes.", "No.", "Ask someone else first.", "Would you believe me if I said I don't know?")
##     phenny.say(random.choice(answers))
## questions.rule = ('$nick', r'(?i)(did|are|is|can|what|where|when|why|will).*$')
#
#
#def simon(phenny, input):
#    if random.choice(range(3)) == 1:
#        simon = ("Who's this Simon guy?", "fail", "Simon says wah wah wah", "Simon Schmimon", "LOL", "Simon make me a sandwich", "I could do that for you.", "Still trying to get Simon to do stuff, eh?")
#        phenny.say(random.choice(simon))
#simon.rule = r'(?i)simon.*$'
#
#
#def not_me(phenny, input):
#    if random.choice(range(3)) == 1:
#        not_me = ("If not me, then who?", "Not your face.", "NOT YOU!", "I know, just... uhh... look at that bird!")
#        phenny.say(random.choice(not_me))
#not_me.rule = r'^(?i)not you$'
#
#
#def awesome(phenny, input):
#    if random.choice(range(3)) == 1:
#        awesome_sauce = ("Awesome sauce!", "King awesome, reporting for duty.", "Awesome is as awesome does.")
#        phenny.say(random.choice(awesome_sauce))
#awesome.rule = r'(?i).awesome.'
#
#
#def ignore(phenny, input):
#    ignore_him = ("My pleasure", "I already am", "I've tried, it doesn't work.", "I'd rather ignore you.")
#    phenny.say(random.choice(ignore_him))
#ignore.commands = ['ignore']