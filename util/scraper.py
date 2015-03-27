from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse


class ScrapeTrivia():
    name = 'Random Trivia'

    trivia_site = 'http://www.randomtriviagenerator.com/'
    soup = BeautifulSoup(urllib.request.urlopen(trivia_site))
    questions = soup.find_all()