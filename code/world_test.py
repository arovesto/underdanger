import unittest

from board import create_board
from player import Player
from world import World

class WorldTest(unittest.TestCase):
    def test_add(self):
        w = World()
        p = Player('Petrovich')
        self.assertEqual(len(w.mobs), 0)
        w.add(p, (100, 121))
        self.assertEqual(len(w.mobs), 1)
        self.assertEqual(p.position, (100, 121))
        self.assertEqual(p.world, w)
        self.assertEqual(w.mobs[(100, 121)], p)
        
    def test_can_move(self):
        w = World()
        p = Player('Petr')
        w.add(p, (0, 0))
        w.add_board(create_board([".#e"]))        
        
        self.assertFalse(w.can_move(p, (-5, 1)))
        self.assertFalse(w.can_move(p, (15, 1)))

        self.assertFalse(w.can_move(p, (0, 1)))
        self.assertTrue(w.can_move(p, (0, 2)))
        
    def test_create_player(self):
        w = World()
        w.add_board(create_board(["...", "...", "..."]))        

        p = w.create_player((0, 0), 'Medium fighter', "Vasya")
        self.assertEqual(p.name, "Vasya")
        self.assertEqual(p.position, (0, 0))
        self.assertEqual(w.mobs[(0, 0)], p)
        
        self.assertEqual(p.world, w)
        self.assertEqual(p.position, (0, 0))

        p2 = w.create_player((2, 2), 'Medium fighter', "Petya")
        self.assertEqual(w.mobs[(0, 0)], p)
        self.assertEqual(w.mobs[(2, 2)], p2)

    def test_is_occupied(self):
        w = World()
        w.add_board(create_board(["...."]))        

        w.create_warrior((0, 1))
        w.create_archer((0, 2))
        w.create_player((0, 3), 'Medium fighter', "Vasya")
        self.assertFalse(w.is_occupied((0, 0)))
        self.assertTrue(w.is_occupied((0, 1)))
        self.assertTrue(w.is_occupied((0, 2)))
        self.assertTrue(w.is_occupied((0, 3)))
        
    def test_has_player_at(self):
        w = World()
        w.add_board(create_board(["...."]))        

        self.assertIsNotNone(w.has_player_at((0, 0)))
        self.assertFalse(w.has_player_at((0, 0)))
        self.assertFalse(w.has_player_at((0, 1)))

        w.create_player((0, 0), 'Medium fighter', "Vasya")
        self.assertTrue(w.has_player_at((0, 0)))
        self.assertFalse(w.has_player_at((0, 1)))            

if __name__ == '__main__':
    unittest.main()
