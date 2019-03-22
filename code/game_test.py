import unittest

from game import Game
        
class GameTest(unittest.TestCase):
    def test_run_action(self):
        g = Game(names = ['Vasya'], classes=['Medium fighter'], shape = (5, 5),
                 start_position = (0, 0), exit_position = (4, 4))
        p = g.action_player
        self.assertEqual(p.position, (0, 0))
        self.assertEqual(p.ap, p.max_ap)
        
        g.run_action('move right')
        
        self.assertEqual(p.position, (0, 1))
        self.assertEqual(p.ap, p.max_ap - 1)

if __name__ == '__main__':
    unittest.main()
