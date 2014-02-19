import re

def sanitize_message(message):
    return re.sub('[\"\']', '', message.lower())

