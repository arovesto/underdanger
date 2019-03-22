import unittest

from merchant import Merchant
from player import Player
from items import normal_heal_potion

class MerchantTest(unittest.TestCase):
    def test_show_items(self):
        m = Merchant().start_equip()
        self.assertEqual(m.show_items()[0:13], 'Merchant sold')
    
    def test_sold(self):
        m = Merchant().start_equip()
        p = Player('Petyka')
        c = m.sold(p, 'healpotion')
        self.assertEqual(p.money, -15)
        self.assertEqual(p.inventory[0].name, normal_heal_potion().name)
        self.assertEqual(c, 'Petyka buy healpotion for 15')
    
if __name__ == '__main__':
    unittest.main()
