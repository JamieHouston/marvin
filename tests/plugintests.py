from unittest import TestCase
from plugins.gitty import GithubHelper


class TestWhoIs(TestCase):
    def test_user_is_on_team(self):
        # how do I test the regex...???