import unittest


class FlowBotTests(unittest.TestCase):
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
