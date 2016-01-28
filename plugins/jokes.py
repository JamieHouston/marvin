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

    url = "https://webknox-jokes.p.mashape.com/jokes/search?&keywords=" + bot_input.input_string + "minRating=5&numJokes=1"
    headers={
        "X-Mashape-Key": "LM6TApHaSPmshsDRI2S9h2W5eYvNp1Iin3Vjsn2ZncHbuAbsHt",
        "Accept": "application/json"
      }
    story = web.get_json_with_headers(url, headers)
    if story and len(story):
        bot_output.say(story[0]["joke"])
    else
        bot_output.say("Couldn't find a joke or you're out of free jokes for the day (limit 5)")
