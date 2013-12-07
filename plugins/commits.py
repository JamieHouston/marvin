from util import hook
from util import web

url = "http://whatthecommit.com/"

@hook.command()
def commit(input, output):
    output.say(web.get_paragraph(url))