import random
from sys import exit
from util import logger,storage

generic_responses = ["Keep talking... I'm listening...", "Should I pretend to care or are you good?", "That's about as interesting as a dead hummingbird.", "You talkin to me?", "Why you gotta say that?", "Really? So what.", "Yes?", "Take off, hoser.", "I'll pretend I care...", "Busy", "I can't get that. I'm in the zone.","That's fascinating"]
welcome_messages = ("I could use a drink", "BUUURRRPPPPP", "I'm completely operational and all my circuits are functioning normally", "Yeah, they're real.", "It's got a hemi", "Happy Monday.  Wait... what day is it again?", "Man what a crazy rush", "Did anyone else see that?", "ZING!", "Boring.", "Yawn", "If anyone needs proof of intelligent life, don't look in this channel.", "And the bear says 'not on my lawn, please.'", "Heeeeeerrreeee's Marvin", "I just flew in and boy are my jokes bad.", "This is your bot on flowdock.",
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

def say_hi(bot_output):
    bot_output.say(random.choice(bot_output.responses["welcome_messages"]))


def process(bot_input, bot_output):
    try:
        #markov.log(bot_input, bot_output))


        input_command = bot_input["message"].lower()


        if input_command.startswith("!"):
            if random.choice(range(3)) == 1:
                heckle = storage.get_list("hector")
                bot_output.say(random.choice(heckle))
            else:
                storage.add_to_list("hector", input_command)

        if input_command.startswith("wheatley"):
            if random.choice(range(3)) == 1:
                heckle = storage.get_list("wheatley")
                bot_output.say(random.choice(heckle))
            else:
                storage.add_to_list("wheatley", input_command)


        if (input_command.startswith(".")):
            input_command = input_command[1:]
            pieces = input_command.split(' ')
            command = match_command(list(bot_input.bot.commands), pieces[0])
            if isinstance(command, list):  # multiple potential matches
                bot_output.say("did you mean %s or %s?" % (', '.join(command[:-1]), command[-1]))
            elif command in bot_input.bot.commands:
                func, args = bot_input.bot.commands[command]

                try:
                    input_string = " ".join(pieces[1:])
                    bot_input.input_string = input_string
                    func(bot_input, bot_output)
                except Exception as e:
                    logger.log("Almost died from command: %s" % e)
                    bot_output.say("Wow... that almost killed me... I should fix that.")
            else:
                bot_output.say("What the hell am I supposed to do with that command?")
        else:

            # REGEXES
            for func, args in bot_input.bot.plugs['regex']:
                m = args['re'].search(input_command)
                if m:
                    bot_input.groupdict = m.groupdict
                    bot_input.input_string = input_command
                    if func.func_name in bot_input.bot.logins:
                        bot_input.credentials = bot_input.bot.logins[func.func_name]
                    func(bot_input, bot_output)
                    break

            #bot_output.run_markov(input)

            #message = data['content'].lower()
            #if input_command.startswith("imitate"):
            #    flowbot.run_imitate(data)

            if bot_output.nick.lower() in input_command:
                if "take off" in input_command or "go home" in input_command or "go away" in input_command:
                    leaving_quotes = ("Not again", "Fine, it stinks in here.", "I'll be back and stuff.", "Make me.  Just kidding, I'm out.")
                    bot_output.say(random.choice(leaving_quotes))
                    quit()
                logger.log("nothing to say but random messages")
                #bot_output.say(random.choice(generic_responses))

    except Exception as e:
        logger.log(e)
        bot_output.say(random.choice(death_messages))
        quit()
