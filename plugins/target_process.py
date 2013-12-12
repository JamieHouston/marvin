from util import hook
import base64
import urllib2
import urllib

class Target_Process():
    user = ''
    password = ''
    tp_uri = ''

    def __init__(self, tp_name, username, password):
        self.data = []
        self.user = username
        self.password = password
        self.tp_uri = tp_name

    def get_object(self):
        auth = base64.encodestring("%s:%s" % (self.user, self.password)).strip()
        request = urllib2.Request(self.tp_uri)
        request.add_header("Authorization", "Basic %s" % auth)
        response = urllib2.urlopen(request)
        return response.read()

@hook.regex(r'(tp recent)')
def target_process(bot_input, bot_output):
    tp = Target_Process(bot_input.credentials["url"], bot_input.credentials["login"], bot_input.credentials["password"])
    bot_output.say(tp.get_object())