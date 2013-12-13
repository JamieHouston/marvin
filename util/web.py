import urllib2, base64, urllib
from bs4 import BeautifulSoup
import json
import random


def build_request(url, username, password):
    request = urllib2.Request(url)
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    return request


def get_title(url):
    try:
        soup = BeautifulSoup(urllib2.urlopen(url))
        return soup.title.string
    except:
        return None
        #return "Not logged in or bad url"

def get_text(url):
    try:
        soup = BeautifulSoup(urllib2.urlopen(url))
        return soup.string
    except:
        error_messages = ("No way can I do that", "Why would I want to do that?", "Bank error in your favor", "You trying to kill me with that request??")
        return random.choice(error_messages)


def get_json(url, username, password):
    request = build_request(url, username, password)
    page = urllib2.urlopen(request)
    data = page.read()
    decoded_data = json.loads(data)
    return decoded_data


def post_json(url, username, password, **kwargs):
    request = build_request(url, username, password)
    request.add_data(urllib.urlencode(kwargs))

    page = urllib2.urlopen(request)
    data = page.read()
    if (data):
        return json.loads(data)
    return data
