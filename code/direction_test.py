import unittest

from direction import UP

class DirectionTest(unittest.TestCase):
    def test_go(self):
        p = (2, 3)
        q = UP.go(p)
        self.assertEqual(q, (1, 3))

if __name__ == '__main__':
    unittest.main()
