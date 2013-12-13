import time
import random
import sys
from util import logger,storage
from plugins import markov, chat

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
    # try:
    input_command = bot_input["message"].lower()

    if input_command == "shut up":
        bot_output.say("SHUTTING UP")
        time.sleep(30)
        return

    direct_message = bot_output.nick.lower() in input_command

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
        if not direct_message:
            markov.handle(bot_input, bot_output)

        if (direct_message or bot_output.chattiness > random.random()):
        # REGEXES
            for func, args in bot_input.bot.plugs['regex']:
                m = args['re'].search(bot_input["message"])
                if m:
                    # todo: update groupdict with inp
                    bot_input.groupdict = m.groupdict
                    bot_input.inp = m.groupdict()
                    bot_input.input_string = input_command
                    if func.func_name in bot_input.bot.credentials:
                        bot_input.credentials = bot_input.bot.credentials[func.func_name]
                    func(bot_input, bot_output)
                    break

            if direct_message and bot_output.master.lower() in bot_input.nick.lower():
                if "take off" in input_command or "go home" in input_command or "go away" in input_command:
                    try:
                        bot_output.say(random.choice(bot_output.responses["death_messages"]))
                    except:
                        logger.log("Too stupid to quit.")
                    sys.exit("later")

            logger.log("nothing to say but random messages")
            bot_input.message = bot_input.message.replace(bot_output.nick.lower(), '')
            #chat.eliza(bot_input, bot_output)

    # except:
    #     logger.log("dying")
    #     bot_output.say(random.choice(bot_output.responses["death_messages"]))
