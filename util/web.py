from bs4 import BeautifulSoup
import random
import requests


def get_title(url):
    try:
        soup = BeautifulSoup(requests.get(url))
        return soup.title.string
    except:
        return None
        #return "Not logged in or bad url"

def get_text(url):
    try:
        response = requests.get(url)
        return response.text
    except:
        error_messages = ("No way can I do that", "Why would I want to do that?", "Bank error in your favor", "You trying to kill me with that request??")
        return random.choice(error_messages)


def get_json(url, username=None, password=None):
    response = requests.get(url, auth=(username, password), params={'format': 'json'})
    if response and response.text:
        return response.json()
    return None


def post_json(url, username, password, **kwargs):
    response = requests.post(url, auth=(username, password), data=kwargs)
    if response and response.json:
        return response.json()
    return response.text
