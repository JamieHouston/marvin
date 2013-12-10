from util import hook

@hook.regex("what(')?s the command for (?P<command_name>\w*)")
def command(bot_input, bot_output):
    if "dbdeploy" in bot_input.input_string:
        bot_output.say("For creating:")
        bot_output.say("DbDeployConsole.exe /eps /eds /els /create /ppmServers=. /PPM=PPM6_Development")
        bot_output.say("For updating:")
        bot_output.say("DbDeployConsole.exe /eps /eds /els /ppmServers=<ppmDatabaseServer> /ppm=PPM6_Development")
        bot_output.say("For servername, use period (.) or, in sql query window, run 'SELECT @@SERVERNAME'")
