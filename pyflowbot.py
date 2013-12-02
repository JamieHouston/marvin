import marvin
from flowdock import JSONStream, Chat, TeamInbox


#config = ConfigParser.ConfigParser()
#config.read('apikey.cfg')

#FLOW_USER_API_KEY = config.get('DEFAULT', 'FLOW_USER_API_KEY')
#FLOW_TOKEN = config.get('DEFAULT' , 'FLOW_TOKEN' )
FLOW_TOKEN = '57bb67a6b0a96d3da3ec3ab8a236d2de'
FLOW_USER_API_KEY = '7a2cf3eba9207150b531577266725c4e'
HR_FLOW = 'daptiv/hr'

debug = False
def send_message(msg):
    chat = Chat(FLOW_TOKEN)
    chat.post(msg, 'Marvin')

def parse_stream():
    stream = JSONStream(FLOW_USER_API_KEY)
    gen = stream.fetch([HR_FLOW], active=True)
    for data in gen:
    # do something with `data`
        if debug:
            print data
        if type(data) == dict and data['event'] == "message" and ('external_user_name' not in data or data['external_user_name'] != 'Marvin'):
            message = data['content'].lower()
            if message.startswith("marvin"):
                if "take off" in message:
                    send_message("Later losers.")
                    quit()
                response = marvin.respond(message)
                print response
                if response and len(response):
                    print "responding with: ", response
                    send_message(response)
                else:
                    print "not responding"

def main():
    send_message(marvin.say_hi())
    parse_stream()

if __name__ == "__main__":
    main()
