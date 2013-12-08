import unittest


class MarvinTests(unittest.TestCase):

    def test_match_command(self):
        from core import marvin
        good_command = "target"
        bad_command = "bla"
        commands= [good_command,"not"]

        result = marvin.match_command(commands, good_command)
        self.assertEquals(good_command, result)
        self.assertIsNone(marvin.match_command(commands, bad_command))

def main():
    unittest.main()

if __name__ == '__main__':
    main()