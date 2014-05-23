import re

def sanitize_message(message):
    return re.sub('[\"\']', '', message.lower())


def is_int(text):
    try:
        int(text)
        return True
    except:
        return False


def strip(text):
    return ''.join([c for c in text if c.isalpha()])


def equal_letters(first, second):
    return strip(first) == strip(second)