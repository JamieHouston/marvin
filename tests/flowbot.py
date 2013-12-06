import unittest
from core import flowbot

class TestParser(unittest.TestCase):
    @staticmethod
    def get_test_config():
        config = {
            "flow_user_api_key": "test_token",
            "flow_token": "test_token",
            "channels": "[test/test]",
            "debug": "False",
            "nick": "testcase"
        }
        return config

    def test_match_command(self):
        command = "target"

        commands= ["target","not"]
        result = flowbot.match_command(commands, command)
        self.assertEquals(command, result)