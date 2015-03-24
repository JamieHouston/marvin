from urllib import request
import random
import json
from external import requests
from external.bs4 import BeautifulSoup

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


def get_json_with_querystring(url, params):
    r = requests.get(url, params=params)
    if r.text:
        return r.text
    return None


def get_json(url, username=None, password=None):
    data = get_raw(url, username, password)
    if data:
        return json.loads(data)
    return None


def get_raw(url, username=None, password=None):
    raw_request = request.build_request(url, username, password)
    page = request.urlopen(raw_request)
    data = page.read().decode("utf-8-sig")
    if data:
        return data
    return None


def post_json_secure(url, token, body):
    headers = {
        'Authorization': 'Bearer {}'.format(token),
        'Accept-Encoding': 'gzip'
    }
    return requests.post(url, data=body, headers=headers)


def get_json_secure(url, token):
    headers = {
        'Authorization': 'Bearer {}'.format(token),
        'Accept-Encoding': 'gzip'
    }
    data = requests.get(url, headers=headers)
    if data:
        return json.loads(data.text)
    return None

def post_json(url, username, password, **kwargs):
    response = requests.post(url, auth=(username, password), data=kwargs)
    if response and response.json:
        return response.json()
    return response.text

def post_json(url, body):
    return requests.post(url, data=json.dumps(body))
