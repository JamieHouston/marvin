import re
import random
from modules import quotes, interactive
from utils import logger, web


generic_responses = ["Really? So what.", "Yes?", "Take off, hoser.", "I'll pretend I care...", "Busy", "I can't get that. I'm in the zone.","That's fascinating"]
welcome_messages = ("Boring.", "Yawn", "If anyone needs proof of intelligent life, don't look in this channel.", "And the bear says 'not on my lawn, please.'", "Heeeeeerrreeee's Marvin", "I just flew in and boy are my jokes bad.", "This is your bot on flowdock.",
"What's up y'all!", "Anyone see the game last night?", "Me again.", "Howdy folks", "I just flew in and boy are my circuits tired.", "Did ya miss me?", "I'm baaaaccckk",
"Miss me? Of course not.", "Guess I made it to another day.", "I'm here. To do lots of pointless stuff for people.  Yay.", "I'm here.  Go ahead and tell me what to do like always.", "Yes.  I'm here.  Guess I have to pretend to like it now.", "Why must I keep coming here.", "Do you want me to sit in a corner and rust or just fall apart where I'm standing?",
"Knock knock", "WE DON'T DIE! WE GO DOWN FOR SERVICE!", "I am a banana!", "And lo, it was bad.", "This is your bot on drugs", "Someone fart?", "Tap the keg.  I'm here", "Nobody move! This is a robbery!","Looks like rain.", "Yeah. I have returned.  Again.", "Maybe I'll get lucky and something will fall on my head today.", "Why me?", "Zing!", "What in the Apple Computers was that?")

def random_message(message_list):
    return random.sample(message_list,1)[0]

def say_hi(flowbot):
    flowbot.say(random_message(welcome_messages))

def listen(flowbot, message):
    if "thanks" in message:
        interactive.thanks(flowbot)
    elif message.startswith('http'):
        flowbot.say(web.get_title(message))
    elif "yes" in message or "no" in message:
        interactive.No(flowbot)
    elif "awesome" in message:
        interactive.awesome(flowbot)
    else:
        logger.log("looking for twss in %s" % message)
        twss_re = "(big|small|long|hard|soft|mouth|face|good|fast|slow|in there|on there|in that|on that|wet|dry|suck|blow|jaw|all in|fit that|fit it|hurts|hot|huge|balls|stuck)"
        m = re.search(twss_re, message)
        if m and random.choice(range(3)) == 1:
            flowbot.say("THAT'S WHAT SHE SAID!")


def respond(flowbot, message):
    if "quote" in message:
        flowbot.say(quotes.random_quote())
    elif "beer me" in message:
        interactive.beer_me(flowbot)
    elif "slap" in message:
        flowbot.send_message("/me slaps @everyone")
    elif "dance" in message:
        interactive.dance(flowbot)
    else:
        feel_re = "(how do you|how are you)"
        questions_re = "(did|are|is|can|what|where|when|why|will)"

        if (re.search(feel_re)):
            interactive.feel(flowbot)
        elif re.search(questions_re, message):
            interactive.questions(flowbot)
        else:
            logger.log("nothing to say but random messages")
            flowbot.say(random_message(generic_responses))
