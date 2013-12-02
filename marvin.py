import random
from modules import quotes

generic_responses = ["Really? So what.", "Yes?", "Take off, hoser.", "I'll pretend I care...", "Busy", "I can't get that. I'm in the zone.","That's fascinating"]
welcome_messages = ["Boring.", "Yawn", "If anyone needs proof of intelligent life, don't look in this channel.", "And the bear says 'not on my lawn, please.'", "Heeeeeerrreeee's Marvin", "I just flew in and boy are my jokes bad.", "This is your bot on flowdock."]

def random_message(message_list):
    return random.sample(message_list,1)[0]

def say_hi():
    return random_message(welcome_messages)

def respond(message):
        if "quote" in message:
            return quotes.random_quote()
    #elif random.random() < 0.5:
        return random_message(generic_responses)
