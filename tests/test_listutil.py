import unittest

from util import listutil


class Test_listutil(unittest.TestCase):

    def test__object_counter(self):
        oc = listutil.ObjectCounter()
        self.assertEqual(list(oc.get().items()), [])

        oc.add("abc")
        oc.add('kj')
        oc.add('dws')
        oc.add('kj')
        oc.add('abcd')
        oc.add('abc')
        oc.add('abc')

        self.assertEqual(sorted(list(oc.get().items())), [('abc', 3), ('abcd', 1), ('dws', 1), ('kj', 2)])


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main()