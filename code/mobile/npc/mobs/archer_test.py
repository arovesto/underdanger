import unittest

from code.mobile.npc.mobs.archer import Archer
from code.geometry.direction import RIGHT
from world.world import World
from world.board.board import create_board


class ArcherTest(unittest.TestCase):
    def test_find_direction_on_player(self):
        w = World()
        a = Archer()
        w.add(a, (0, 0))
        w.add_board(create_board(['...........', '..']), exits=None)
        self.assertIsNone(a.find_direction_on_player())

        w.create_player((1, 1), 'рыцарь', "Vasya is on diagonal")
        self.assertIsNone(a.find_direction_on_player())

        w.create_player((0, 20), 'рыцарь', "Vasya is too far")
        self.assertIsNone(a.find_direction_on_player())

        w.create_player((0, 2), 'рыцарь', "Petya is near")
        self.assertEqual(a.find_direction_on_player(), RIGHT)


if __name__ == '__main__':
    unittest.main()
