from util import dictionaryutils
import unittest

class UtilTests(unittest.TestCase):
    def access_dictionary_keys_by_property(self):
        start = {"first":"post"}
        end = dictionaryutils.Blob(**start)
        self.assertEquals(end.first, start["first"])


def main():
    unittest.main()

if __name__ == '__main__':
    main()