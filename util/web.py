import urllib2, base64
from bs4 import BeautifulSoup
import json


def get_title(url):
    try:
        soup = BeautifulSoup(urllib2.urlopen(url))
        return soup.title.string
    except:
        return "Not logged in or bad url"

def get_paragraph(url):
    try:
        soup = BeautifulSoup(urllib2.urlopen(url))
        return soup.p.string
    except:
        return "Bank error in your favor"


def get_json(url, username, password):
    request = urllib2.Request(url)
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    #result = urllib2.urlopen(request)

    #request = urllib2.Request(url)
    page = urllib2.urlopen(request)
    data = page.read()
    decoded_data = json.loads(data)
    return decoded_data