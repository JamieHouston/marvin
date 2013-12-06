def db_deploy(flowbot):
    flowbot.say("For creating:")
    flowbot.say("DbDeployConsole.exe /eps /eds /els /create /ppmServers=. /PPM=PPM6_Development")
    flowbot.say("For updating:")
    flowbot.say("DbDeployConsole.exe /eps /eds /els /ppmServers=<ppmDatabaseServer> /ppm=PPM6_Development")
    flowbot.say("For servername, use period (.) or, in sql query window, run 'SELECT @@SERVERNAME'")
