import re
import random
#from modules import quotes, interactive, daptiv_commands
from modules import interactive
from plugins import daptiv_commands
from util import logger, web

generic_responses = ["Keep talking... I'm listening...", "Should I pretend to care or are you good?", "That's about as interesting as a dead hummingbird.", "You talkin to me?", "Why you gotta say that?", "Really? So what.", "Yes?", "Take off, hoser.", "I'll pretend I care...", "Busy", "I can't get that. I'm in the zone.","That's fascinating"]
welcome_messages = ("Yeah, they're real.", "It's got a hemi", "Happy Monday.  Wait... what day is it again?", "Man what a crazy rush", "Did anyone else see that?", "ZING!", "Boring.", "Yawn", "If anyone needs proof of intelligent life, don't look in this channel.", "And the bear says 'not on my lawn, please.'", "Heeeeeerrreeee's Marvin", "I just flew in and boy are my jokes bad.", "This is your bot on flowdock.",
"What's up y'all!", "Anyone see the game last night?", "Me again.", "Howdy folks", "I just flew in and boy are my circuits tired.", "Did ya miss me?", "I'm baaaaccckk",
"Miss me? Of course not.", "Guess I made it to another day.", "I'm here. To do lots of pointless stuff for people.  Yay.", "I'm here.  Go ahead and tell me what to do like always.", "Yes.  I'm here.  Guess I have to pretend to like it now.", "Why must I keep coming here.", "Do you want me to sit in a corner and rust or just fall apart where I'm standing?",
"Knock knock", "WE DON'T DIE! WE GO DOWN FOR SERVICE!", "I am a banana!", "And lo, it was bad.", "This is your bot on drugs", "Someone fart?", "Tap the keg.  I'm here", "Nobody move! This is a robbery!","Looks like rain.", "Yeah. I have returned.  Again.", "Maybe I'll get lucky and something will fall on my head today.", "Why me?", "Zing!", "What in the Apple Computers was that?")

def match_command(commands, command):

    # do some fuzzy matching
    prefix = filter(lambda x: x.startswith(command), commands)
    if len(prefix) == 1:
        return prefix[0]
    elif prefix and command not in prefix:
        return prefix

    return command

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
    elif "fail" in message:
        interactive.fail(flowbot)
    elif "not you" in message:
        interactive.not_me(flowbot)
    else:
        logger.log("looking for twss in %s" % message)
        laugh_re = "(lol|haha|ha ha|rofl|hehe|rolfmao|lmao)"
        twss_re = "(big|small|long|hard|soft|mouth|face|good|fast|slow|in there|on there|in that|on that|wet|dry|suck|blow|jaw|all in|fit that|fit it|hurts|hot|huge|balls|stuck)"

        if re.search(laugh_re, message):
            interactive.laugh(flowbot)
        elif re.search(twss_re, message):
            if random.choice(range(3)) == 1:
                flowbot.say("THAT'S WHAT SHE SAID!")


def respond(flowbot, message):
    #if "quote" in message:
    #    flowbot.say(quotes.random_quote())
    #if "dbdeploy" in message or "update database" in message:
    #    daptiv_commands.db_deploy(flowbot)
    if "beer me" in message:
        interactive.beer_me(flowbot)
    elif "slap" in message:
        flowbot.send_message("/me slaps @everyone")
    elif "dance" in message:
        interactive.dance(flowbot)
    elif "sandwich" in message:
        interactive.sandwich(flowbot, message)
    elif "ignore" in message:
        interactive.ignore(flowbot)
    elif "welcome back" in message:
        interactive.welcome_back(flowbot)
    else:
        feel_re = "(how do you|how are you)"
        questions_re = "(did|are|is|can|what|where|when|why|will)"

        if re.search(feel_re, message):
            interactive.feel(flowbot)
        elif re.search(questions_re, message):
            interactive.questions(flowbot)
        else:
            logger.log("nothing to say but random messages")
            flowbot.say(random_message(generic_responses))

def input(input_command, bot, flowbot):
    try:
        if (input_command.startswith(".")):
            input_command = input_command[1:]
            pieces = input_command.split()
            command = match_command(list(bot.commands), pieces[0])
            if isinstance(command, list):  # multiple potential matches
                flowbot.say("did you mean %s or %s?" % (', '.join(command[:-1]), command[-1]))
            elif command in bot.commands:
                func, args = bot.commands[command]

                try:
                    result = func(" ".join(pieces[1:]))
                    flowbot.say(result)
                except:
                    logger.log("Almost died from command")
                    #flowbot.say("Wow... that almost killed me... I should fix that.")
        else:
            # REGEXES
            for func, args in bot.plugs['regex']:
                m = args['re'].search(input_command)
                if m:
                    result = func(input_command)
                    flowbot.say(result)
                    continue;

            #flowbot.run_markov(data)

            #message = data['content'].lower()
            #if input_command.startswith("imitate"):
            #    flowbot.run_imitate(data)

            if "marvin" in input_command:
                if "take off" in input_command or "go home" in input_command or "go away" in input_command:
                    leaving_quotes = ("Not again", "Fine, it stinks in here.", "I'll be back and stuff.", "Make me.  Just kidding, I'm out.")
                    flowbot.say(random_message(leaving_quotes))
                    quit()
                respond(flowbot, input_command)
            else:
                listen(flowbot, input_command)
    except Exception as e:
        logger.log(e)
        flowbot.say("My mind is fading... so cold... so dark...")
        quit()
