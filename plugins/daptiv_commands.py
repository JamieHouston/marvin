from util import hook

@hook.regex("command for (?P<command_name>\w*)")
def db_deploy(input, output):
    output.say("For creating:")
    output.say("DbDeployConsole.exe /eps /eds /els /create /ppmServers=. /PPM=PPM6_Development")
    output.say("For updating:")
    output.say("DbDeployConsole.exe /eps /eds /els /ppmServers=<ppmDatabaseServer> /ppm=PPM6_Development")
    output.say("For servername, use period (.) or, in sql query window, run 'SELECT @@SERVERNAME'")
