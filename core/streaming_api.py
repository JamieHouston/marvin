# coding: utf-8
import json
import requests
from util import logger
import traceback
import sys

STREAMING_API_URL = "https://stream.gitter.im/v1/rooms/{room_id}/chatMessages"
DEFAULT_CONTENT_TYPE = 'application/json'


class StreamingAPI(object):
    ALLOWED_STATUSES = (True, 'idle', None)
    STREAM_CHUNK_SIZE = 1

    def __init__(self, personal_api_token, room_id, accept=DEFAULT_CONTENT_TYPE):
        self.api_url = STREAMING_API_URL.format(room_id=room_id)
        self.personal_api_token = personal_api_token
        self.accept = accept
        self.active = None
        self.headers = {
            'content-type': DEFAULT_CONTENT_TYPE,
            'accept': self.accept,
            'Authorization': 'Bearer %s' % self.personal_api_token
        }
        self.connection = None

    def __repr__(self):
        return "%s(%s, %s, %s, %s) instance at %s" % (self.__class__.__name__, self.personal_api_token, self.flows, self.active, self.accept, hex(id(self)))

    @property
    def stream(self):
        if not self.connection or not self.connection.ok:
            self.connection = requests.get(self.api_url, headers=self.headers, stream=True)
            if not self.connection.ok:
                self.connection.raise_for_status()
        return self.connection

    def fetch(self):
        for line in self.stream.iter_lines(self.STREAM_CHUNK_SIZE):
            if line and len(line.strip()) and line != ':':
                try:
                    result = json.loads(line)
                    yield result
                except Exception as e:
                    print("error parsing line")
                    print(line)
                    print(traceback.format_exc())
                    for info in sys.exc_info():
                        logger.log("error info: " + str(info))


def JSONStream(personal_api_token, room_id):
    return StreamingAPI(personal_api_token, room_id)
