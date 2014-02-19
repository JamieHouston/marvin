from util import hook
import time

first_time = True

@hook.command
def trivia(bot_input, bot_output):
    bot_output.say("WOOO WOOO WOOO WOOO WOOO")
    bot_output.say("Starting Trivia Round.  First correct answer gets 5 points.  First incorrect answer gets a slap in the face")
    bot_output.say("First question")
    time.sleep(2)
    bot_output.say("Who farted.")
    time.sleep(2)
    bot_output.say("no, really... who farted?")
    time.sleep(2)
    bot_output.say("I'm not playing until someone tells me...")
