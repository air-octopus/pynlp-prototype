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


    def test__str_extract_same_beg(self):
        self.assertEqual(strutil.str_extract_same_beg('', ''), ('', '', ''))
        self.assertEqual(strutil.str_extract_same_beg('a', ''), ('', 'a', ''))
        self.assertEqual(strutil.str_extract_same_beg('', 'a'), ('', '', 'a'))
        self.assertEqual(strutil.str_extract_same_beg('abc', ''), ('', 'abc', ''))
        self.assertEqual(strutil.str_extract_same_beg('', 'abc'), ('', '', 'abc'))

        self.assertEqual(strutil.str_extract_same_beg('abc', 'def'), ('', 'abc', 'def'))
        self.assertEqual(strutil.str_extract_same_beg('abc', 'a'), ('a', 'bc', ''))
        self.assertEqual(strutil.str_extract_same_beg('abc', 'abd'), ('ab', 'c', 'd'))
        self.assertEqual(strutil.str_extract_same_beg('abc', 'abcdef'), ('abc', '', 'def'))
        self.assertEqual(strutil.str_extract_same_beg('abc', 'abdef'), ('ab', 'c', 'def'))
        self.assertEqual(strutil.str_extract_same_beg('', ''), ('', '', ''))


    def test__str_decompose(self):
        dic = {}
        self.assertEqual(strutil.str_decompose('', dic), [])
        self.assertEqual(strutil.str_decompose('rrr', dic), [])

        dic = {'a', 'ab', 'dcd'}
        self.assertEqual(strutil.str_decompose('', dic), [])
        self.assertEqual(strutil.str_decompose('rrr', dic), [])
        self.assertEqual(strutil.str_decompose('aabadcdab', dic), [['a', 'ab', 'a', 'dcd', 'ab']])

        dic = ['a', 'aa', 'aaa']
        res = strutil.str_decompose('aaa', dic, False)
        self.assertTrue(['a', 'a', 'a'] in res)
        self.assertTrue(['aa', 'a'] in res)
        self.assertTrue(['a', 'aa'] in res)
        # self.assertTrue(['aaa'] in res)

        # разрешаем саму строку в результатах
        res = strutil.str_decompose('aaa', dic, True)
        self.assertTrue(['a', 'a', 'a'] in res)
        self.assertTrue(['aa', 'a'] in res)
        self.assertTrue(['a', 'aa'] in res)
        self.assertTrue(['aaa'] in res)


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main()