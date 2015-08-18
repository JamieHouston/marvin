from util import hook, web

@hook.command
def joke(bot_input, bot_output):
    # These code snippets use an open-source library. http://unirest.io/python
    # joke = web.get_json_with_headers(
    #     "https://webknox-jokes.p.mashape.com/jokes/random?maxLength=100",
    #     headers={
    #         "X-Mashape-Key": "LM6TApHaSPmshsDRI2S9h2W5eYvNp1Iin3Vjsn2ZncHbuAbsHt",
    #     "Accept": "application/json"
    #     })
    story = web.get_json("http://webknox.com/api/jokes/random")#?apiKey=bdihdcabiccdmcxpkltuvoeyaqbzcgx")
    bot_output.say("This one's called " + story["title"] + "\n" + story["joke"])