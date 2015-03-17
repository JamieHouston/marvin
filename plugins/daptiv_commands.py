from util import hook

#@hook.regex("what(')?(s| is) the command for (?P<command_name>\w*)", run_always=True)
@hook.regex("dbdeploy", run_always=True)
def command(bot_input, bot_output):
    #if "dbdeploy" in bot_input.input_string:
    result = ["For creating:",
              "DbDeployConsole.exe /eps /eds /els /create /ppmServers=%COMPUTERNAME% /PPM=PPM6_Development",
              "For updating:",
              "DbDeployConsole.exe /eps /eds /els /ppmServers=%COMPUTERNAME% /ppm=PPM6_Development",
              "Remove the /ppm switch to apply to all databases",
              "Remember to use command prompt or escape characters in a shell (like bash)"]
    bot_output.say('\n'.join(result))