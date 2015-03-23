from util import hook
from core import reload, config


@hook.command
def refresh(bot_input, bot_output):
    bot_output.say("Refreshing Plugins")
    reload.reload(bot_input.bot)
    config.config(bot_input.bot)
    bot_output.say("I'm all shiny and new now")