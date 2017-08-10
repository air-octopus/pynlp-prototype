import unittest

from util import strutil


class Test_strutil(unittest.TestCase):

    def test__str_convolution_max(self):
        self.assertEqual(strutil.str_convolution_max('abcd', 'oabqde'), (-1, 3))

    def test__str_split_by_equal(self):
        self.assertEqual(strutil.str_split_by_equal('abc', 'abc', 5),
                         (['abc', ''], ['', 'abc']))
        self.assertEqual(strutil.str_split_by_equal('abc', 'abc', -5),
                         (['', 'abc'], ['abc', '']))
        self.assertEqual(strutil.str_split_by_equal('abc', 'abc', 2),
                         (['ab', 'c', ''], ['', 'a', 'bc']))
        self.assertEqual(strutil.str_split_by_equal('rabcdefgh', 'abcqpmgyli', 1),
                         (['r', 'abc', 'def', 'g', 'h', ''], ['', 'abc', 'qpm', 'g', 'y', 'li']))


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main()