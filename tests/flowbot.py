import unittest
from core.flowbot import FlowBot

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
        bot = {}
        bot.commands= ["target","not"]
        flowbot = FlowBot(TestParser.get_test_config())
        result = flowbot.match_command(command)
        self.assertEquals(command, result)