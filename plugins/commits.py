from util import hook
from util import web

url = "http://whatthecommit.com/"

@hook.command()
def commit(inp):
    return web.get_paragraph(url)