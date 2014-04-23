from util import hook

@hook.regex("what(')?s the command for (?P<command_name>\w*)", run_always=True)
def command(bot_input, bot_output):
    if "dbdeploy" in bot_input.input_string:
        result = ["For creating:",
                  "DbDeployConsole.exe /eps /eds /els /create /ppmServers=%COMPUTERNAME% /PPM=PPM6_Development",
                  "For updating:",
                  "DbDeployConsole.exe /eps /eds /els /ppmServers=%COMPUTERNAME% /ppm=PPM6_Development",
                  "Remove the /ppm switch to apply to all databases"]
        bot_output.say('\n'.join(result))