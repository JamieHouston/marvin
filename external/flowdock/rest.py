import requests

REST_API_URL = "https://api.flowdock.com/{0}/{1}/messages"

class RestAPI(object):
    API_URL = REST_API_URL.format("daptiv","hackday")

    def __init__(self, flow_api_token):
        self.flow_api_token = flow_api_token
        self.api_url = self.API_URL % self.flow_api_token

    def __repr__(self):
        return "%s(%s) instance at %s" % (self.__class__.__name__, self.flow_api_token, hex(id(self)))

    def post(self, data):
        data = dict((k, v) for k, v in data.iteritems() if k != 'self' and v is not None)
        response = requests.post(self.api_url, data=data)
        if not response.ok:
            response.raise_for_status()
        return True
