import unittest

import morpho


class Test_morpho(unittest.TestCase):

    def test__extract_proto_morphemes(self):
        self.assertEqual(morpho.extract_proto_morphemes('rabcdefgh', 'abcqpmgyli'), (['r'], 'abc', ['defgh', 'qpmgyli']))


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main()
