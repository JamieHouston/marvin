import random
from modules import quotes, interactive

generic_responses = ["Really? So what.", "Yes?", "Take off, hoser.", "I'll pretend I care...", "Busy", "I can't get that. I'm in the zone.","That's fascinating"]
welcome_messages = ["Boring.", "Yawn", "If anyone needs proof of intelligent life, don't look in this channel.", "And the bear says 'not on my lawn, please.'", "Heeeeeerrreeee's Marvin", "I just flew in and boy are my jokes bad.", "This is your bot on flowdock."]

def random_message(message_list):
    return random.sample(message_list,1)[0]

def say_hi(flowbot):
    flowbot.say(random_message(welcome_messages))

def respond(flowbot, message):
    #elif random.random() < 0.5:
    if "quote" in message:
        flowbot.say(quotes.random_quote())
    #elif "slap" in message:
    #    flowbot.send_message("/me slaps @everyone")
    elif "thanks" in message:
        interactive.thanks(flowbot)
    elif "yes" in message or "no" in message:
        interactive.No(flowbot)
    elif "beer me" in message:
        interactive.beer_me(flowbot)
    else:
        flowbot.say(random_message(generic_responses))
