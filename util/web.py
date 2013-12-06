import urllib2
from bs4 import BeautifulSoup


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