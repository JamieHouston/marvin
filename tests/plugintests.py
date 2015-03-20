from unittest import TestCase
from plugins import anytag
from plugins.gitty import GithubHelper


class AnyTagTests(TestCase):
    def test_added_to_list(self):
        self.assertEquals(1, 1)


class MarkovTests(TestCase):
    def test_markov_generated_from_pairs(self):
        self.assertEquals(1, 1)


class TestGitty(TestCase):
    def test_get_pull_requests(self):
        gh = GithubHelper()