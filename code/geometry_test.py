import unittest
from geometry import distance, add, manhattan, in_square, square, merge
        
class GeometryTest(unittest.TestCase):
    def test_distance(self):
        self.assertEqual(distance((0, 0), (0, 3)), 3)
        self.assertEqual(distance((1, 1), (4, 5)), 5)
    
    def test_add(self):
        self.assertEqual(add((-1, -1), (1, 1)), (0, 0))
        self.assertEqual(add((20, -4), (0, 124)), (20, 120))

    def test_manhattan(self):
        self.assertEqual(manhattan((1, 0),(10, 0)), 9)
        self.assertEqual(manhattan((-1, -1), (7, 8)), 17)

    def test_in_square(self):
        self.assertTrue(in_square((4, 4), (0, 0), 4))
        self.assertFalse(in_square((5, 4), (0, 0), 4))
        self.assertFalse(in_square((4, 5), (0, 0), 4))

    def test_square(self):
        self.assertEqual(square((1, 1), 0), [(1, 1)])
        self.assertEqual(set(square((1, 1), 1)), {(1, 1), (0, 0), (2, 2), (1, 2), (2, 1), (0, 2),(2, 0), (1, 0), (0, 1)})

    def test_merge(self):
        self.assertEqual(merge([square((1, 1), 1), square((2, 2), 1)]),
                         {(1, 1), (0, 0), (2, 2), (1, 2), (2, 1), (0, 2),(2, 0), (1, 0), (0, 1), (2, 3), (3, 2), (3, 3),
                          (3, 1), (1, 3)})
if __name__ == '__main__':
    unittest.main()