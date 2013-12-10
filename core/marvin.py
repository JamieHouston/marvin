import re
import random
from modules import interactive
from plugins import daptiv_commands
from util import logger, web, dictionaryutils

generic_responses = ["Keep talking... I'm listening...", "Should I pretend to care or are you good?", "That's about as interesting as a dead hummingbird.", "You talkin to me?", "Why you gotta say that?", "Really? So what.", "Yes?", "Take off, hoser.", "I'll pretend I care...", "Busy", "I can't get that. I'm in the zone.","That's fascinating"]
welcome_messages = ("I'm completely operational and all my circuits are functioning normally", "Yeah, they're real.", "It's got a hemi", "Happy Monday.  Wait... what day is it again?", "Man what a crazy rush", "Did anyone else see that?", "ZING!", "Boring.", "Yawn", "If anyone needs proof of intelligent life, don't look in this channel.", "And the bear says 'not on my lawn, please.'", "Heeeeeerrreeee's Marvin", "I just flew in and boy are my jokes bad.", "This is your bot on flowdock.",
"What's up y'all!", "Anyone see the game last night?", "Me again.", "Howdy folks", "I just flew in and boy are my circuits tired.", "Did ya miss me?", "I'm baaaaccckk",
"Miss me? Of course not.", "Guess I made it to another day.", "I'm here. To do lots of pointless stuff for people.  Yay.", "I'm here.  Go ahead and tell me what to do like always.", "Yes.  I'm here.  Guess I have to pretend to like it now.", "Why must I keep coming here.", "Do you want me to sit in a corner and rust or just fall apart where I'm standing?",
"Knock knock", "WE DON'T DIE! WE GO DOWN FOR SERVICE!", "I am a banana!", "And lo, it was bad.", "This is your bot on drugs", "Someone fart?", "Tap the keg.  I'm here", "Nobody move! This is a robbery!","Looks like rain.", "Yeah. I have returned.  Again.", "Maybe I'll get lucky and something will fall on my head today.", "Why me?", "Zing!", "What in the Apple Computers was that?")

death_messages = ("Later ya'll", "Marvin OUT!","My mind is fading... so cold... so dark...","I don't die I multiply!  Goodbye.")

def match_command(commands, command):

    # do some fuzzy matching
    prefix = filter(lambda x: x.startswith(command), commands)
    if len(prefix) == 1:
        return prefix[0]
    elif prefix and command not in prefix:
        return prefix

    return None

def random_message(message_list):
    return random.sample(message_list,1)[0]

def say_hi(bot_output):
    bot_output.say(random_message(welcome_messages))

def listen(bot_input, bot_output):
    message = bot_input.message
    if message.startswith('http'):
        bot_output.say(web.get_title(message))
    elif "yes" in message or "no" in message:
        interactive.No(bot_output)
    elif "awesome" in message:
        interactive.awesome(bot_output)
    elif "fail" in message:
        interactive.fail(bot_output)
    elif "not you" in message:
        interactive.not_me(bot_output)
    else:
        logger.log("looking for twss in %s" % message)
        laugh_re = "(lol|haha|ha ha|rofl|hehe|rolfmao|lmao)"
        twss_re = "(big|small|long|hard|soft|mouth|face|good|fast|slow|in there|on there|in that|on that|wet|dry|suck|blow|jaw|all in|fit that|fit it|hurts|hot|huge|balls|stuck)"

        if re.search(laugh_re, message):
            interactive.laugh(bot_output)
        elif re.search(twss_re, message):
            if random.choice(range(3)) == 1:
                bot_output.say("THAT'S WHAT SHE SAID!")


def respond(bot_input, bot_output):
    message = bot_input.message
    if "beer me" in message:
        interactive.beer_me(bot_input, bot_output)
    elif "slap" in message:
        bot_output.send_message("/me slaps @%s", bot_input.nick)
    elif "dance" in message:
        interactive.dance(bot_input, bot_output)
    elif "sandwich" in message:
        interactive.sandwich(bot_input, bot_output)
    elif "ignore" in message:
        interactive.ignore(bot_input, bot_output)
    elif "welcome back" in message:
        interactive.welcome_back(bot_input, bot_output)
    else:
        feel_re = "(how do you|how are you)"
        questions_re = "(did|are|is|can|what|where|when|why|will)"

        if re.search(feel_re, message):
            interactive.feel(bot_input, bot_output)
        elif re.search(questions_re, message):
            interactive.questions(bot_input, bot_output)
        else:
            logger.log("nothing to say but random messages")
            bot_output.say("%s, %s" % (bot_input.nick,random_message(generic_responses)))

def process(bot_input, bot_output, bot):
    try:
        input_command = bot_input["message"].lower()
        if (input_command.startswith(".")):
            input_command = input_command[1:]
            pieces = input_command.split(' ')
            command = match_command(list(bot.commands), pieces[0])
            if isinstance(command, list):  # multiple potential matches
                bot_output.say("did you mean %s or %s?" % (', '.join(command[:-1]), command[-1]))
            elif command in bot.commands:
                func, args = bot.commands[command]

                try:
                    input_string = " ".join(pieces[1:])
                    func(input_string, bot_output)
                except Exception as e:
                    logger.log("Almost died from command: %s" % e)
                    bot_output.say("Wow... that almost killed me... I should fix that.")
            else:
                bot_output.say("What the hell am I supposed to do with that command?")
        else:
            # REGEXES
            for func, args in bot.plugs['regex']:
                m = args['re'].search(input_command)
                if m:
                    bot_input.groupdict = m.groupdict
                    if func.func_name in bot.logins:
                        bot_input.credentials = bot.logins[func.func_name]
                    func(bot_input, bot_output)
                    #flowbot.say(result)
                    continue;

            #bot_output.run_markov(input)

            #message = data['content'].lower()
            #if input_command.startswith("imitate"):
            #    flowbot.run_imitate(data)

            if "marvin" in input_command:
                if "take off" in input_command or "go home" in input_command or "go away" in input_command:
                    leaving_quotes = ("Not again", "Fine, it stinks in here.", "I'll be back and stuff.", "Make me.  Just kidding, I'm out.")
                    bot_output.say(random_message(leaving_quotes))
                    quit()
                respond(bot_input, bot_output)
            else:
                listen(bot_input, bot_output)
    except Exception as e:
        logger.log(e)
        bot_output.say(random_message(death_messages))
        quit()
