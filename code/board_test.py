import unittest

from board import BoardGenerator, create_board, create_figure, Rectangle, rotate
from square import Square


class BoardTest(unittest.TestCase):
    def test_is_inside(self):
        r = Rectangle((3, 5))

        self.assertTrue(r.is_inside((0, 0)))
        self.assertTrue(r.is_inside((1, 1)))
        self.assertTrue(r.is_inside((2, 2)))
        self.assertTrue(r.is_inside((2, 3)))
        self.assertTrue(r.is_inside((2, 4)))
        self.assertTrue(r.is_inside((0, 4)))
        self.assertTrue(r.is_inside((2, 0)))

        self.assertFalse(r.is_inside((-3, -8)))
        self.assertFalse(r.is_inside((-3, 8)))
        self.assertFalse(r.is_inside((-1, 0)))
        self.assertFalse(r.is_inside((0, -1)))
        self.assertFalse(r.is_inside((3, 3)))
        self.assertFalse(r.is_inside((2, 5)))
        self.assertFalse(r.is_inside((3, 5)))
        
    def test_neighbours(self):
        r = Rectangle((2, 2))
        self.assertEqual(r.neighbours((0, 0)), [(0, 1), (1, 0), (1, 1)])

    def test_rotate_right(self):
        model = create_figure(['...', '.#.', '.#.'])
        rotated = rotate(create_figure(['...', '.##', '...']))
        self.assertEqual(model, rotated)
        
    def test_generate(self):
        b = BoardGenerator((10, 10)).generate()
        
        squares = [b.square((i, j)) for i in range(10) for j in range(10)] 
        floor_count = len([s for s in squares if s.kind == 'floor'])
        wall_count = len([s for s in squares if s.kind == 'wall'])
        grass_count = len([s for s in squares if s.kind == 'grass'])
       
        self.assertTrue(floor_count > 0)
        self.assertTrue(wall_count > 0)
        self.assertTrue(grass_count > 0)
        
    def test_create_board(self):
        lines = ["###",
                 "#..",
                 "#.#"]
        b = create_board(lines)
        self.assertEqual(b.square((0, 0)).kind, 'wall')
        self.assertEqual(b.square((0, 1)).kind, 'wall')
        self.assertEqual(b.square((0, 2)).kind, 'wall')
        self.assertEqual(b.square((1, 0)).kind, 'wall')
        self.assertEqual(b.square((1, 1)).kind, 'floor')
        self.assertEqual(b.square((1, 2)).kind, 'floor')
        self.assertEqual(b.square((2, 0)).kind, 'wall')
        self.assertEqual(b.square((2, 1)).kind, 'floor')
        self.assertEqual(b.square((2, 2)).kind, 'wall')

    def test_create_figure(self):
        lines = ["###",
                 "#..",
                 "#.#"]
        f = create_figure(lines)
        self.assertEqual(f[(0, 0)].kind, 'wall')
        self.assertEqual(f[(0, 1)].kind, 'wall')
        self.assertEqual(f[(0, 2)].kind, 'wall')
        self.assertEqual(f[(1, 0)].kind, 'wall')
        self.assertEqual(f[(1, 1)].kind, 'floor')
        self.assertEqual(f[(1, 2)].kind, 'floor')
        self.assertEqual(f[(2, 0)].kind, 'wall')
        self.assertEqual(f[(2, 1)].kind, 'floor')
        self.assertEqual(f[(2, 2)].kind, 'wall')
    
    def test_add_figure(self):
        g = BoardGenerator((11, 11))
        f = {(0, 0) : Square('wall'), 
             (0, 1) : Square('floor'), 
             (0, -2) : Square('water'),
             (0, -10) : Square('grass')}
        
        g.add_figure((5, 5), f)
        b = g.create_board()
        
        self.assertEqual(b.square((5, 5)).kind, 'wall')
        self.assertEqual(b.square((5, 6)).kind, 'floor')
        self.assertEqual(b.square((5, 3)).kind, 'water')
        
        self.assertFalse((5, -5) in b.squares)

    def test_add_figure_no_override(self):
        g = BoardGenerator((3, 3))
        f = {(0, 0) : Square('wall'), (0, 1) : Square('floor')}
        
        g.add_figure((0, 0), f)
        b1 = g.create_board()
        self.assertEqual(b1.square((0, 0)).kind, 'wall')
        self.assertEqual(b1.square((0, 1)).kind, 'floor')

        g.add_figure((0, 1), f, override = False)
        b2 = g.create_board()
        self.assertEqual(b2.square((0, 1)).kind, 'floor')
        
        g.add_figure((0, 1), f, override = True)
        b3 = g.create_board()
        self.assertEqual(b3.square((0, 1)).kind, 'wall')


if __name__ == '__main__':
    unittest.main()
