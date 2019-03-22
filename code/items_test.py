import unittest

from player import Player
from items import rest_potion

class ItemsTest(unittest.TestCase):
    def test_APRestorePotion(self):
        p = Player("Vasyan")
        p.inventory.append(rest_potion())
        p.ap = 3
        p.max_ap = 10
        self.assertNotEqual(p.ap, p.max_ap)
        p.do_use(rest_potion().name)
        self.assertEqual(p.ap, p.max_ap)
    
if __name__ == '__main__':
    unittest.main()