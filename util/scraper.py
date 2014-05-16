from bs4 import BeautifulSoup
import urllib2

class ScrapeTrivia():
    name = 'Random Trivia'

    trivia_site = 'http://www.randomtriviagenerator.com/'
    soup = BeautifulSoup(urllib2.urlopen(trivia_site))
    questions = soup.find_all()