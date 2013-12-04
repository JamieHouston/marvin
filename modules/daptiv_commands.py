def db_deploy(flowbot):
    flowbot.say("For creating:")
    flowbot.say("DbDeployConsole.exe /eps /eds /els /create /ppmServers=<ppmDatabaseServer> /PPM=AIS_PPM;Sears_PPM")
    flowbot.say("For updating:")
    flowbot.say("DbDeployConsole.exe /eps /eds /els /ppmServers=<ppmDatabaseServer1>;<ppmDatabaseServerN>")
    flowbot.say("For servername, in query window, run 'SELECT @@SERVERNAME'")
