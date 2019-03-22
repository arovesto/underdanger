import unittest

from player import Player
from world import World
from merchant import Merchant
from items import glasses
from weapons import player_knife

class PlayerTest(unittest.TestCase):
    def test_init(self):
        p = Player("Vasyan")
        self.assertEqual(p.name, "Vasyan")

    def test_stats(self):
        p = Player("Vas")
        p.hp = 18
        p.ap = 3
        p.class_ = 'No one'
        self.assertEqual(p.stats(), 'Vas, No one, level 1:\n[HP = 18, AP = 3, Armor = 0]. Money = 0, EXP = 0')
        
    def test_heal(self):
        p = Player("Vas")
        p.max_hp = 20
        p.hp = 18
        p.heal()
        self.assertEqual(p.hp, 20)
    
    def test_do_showshopitems(self):
        w = World()
        p = w.add(Player('Petya'), (0, 0))
        p.do_showshopitems()
        self.assertEqual(p.last_happend, 'Petya asked air about his trades')
        
        m = w.add(Merchant(), (0, 10)).start_equip()
        p.do_showshopitems()
        self.assertEqual(p.last_happend, 'Petya asked air about his trades')
        
        m.position = (0, 1)
        p.do_showshopitems()
        self.assertNotEqual(p.last_happend, ' there no merchants here')
    
    def test_do_share(self):
        p1 = Player('Shtirliz')
        p1_inv_before = p1.inventory
        p1.position = (10, 0)
        p2 = Player('Isaev')
        p2_inv_before = p2.inventory
        p2.position = (0, 0)
        w = World()
        w.mobs[(0, 0)] = p2
        p1.world = w
        p1.inventory += [glasses()]
        p1.do_share('Isaev', 'glasses')
        self.assertEqual(p1.last_happend, 'Shtirliz to far from Isaev')
        self.assertEqual(p2.inventory, p2_inv_before)
        
        p1.position = (0, 0)
        p1.do_share('Isaev', 'glasses')        
        self.assertEqual(p1.last_happend, 'Shtirliz gives glasses to Isaev')
        self.assertEqual(p2.inventory[-1].name, 'glasses')
        self.assertEqual(len(p1.inventory), len(p1_inv_before))
        
        p1.do_share('Isaev', 'glasses')
        self.assertEqual(p1.last_happend, "Shtirliz can't give glasses to Isaev")
    
    def test_do_equip(self):
        p = Player('Petya')
        p.inventory = [player_knife()]
        self.assertIsNone(p.equipment['mainhand'])
        p.do_equip('smallknife')
        self.assertEqual(p.equipment['mainhand'].name, 'smallknife')
        self.assertEqual(p.equipment['mainhand'].user, p)
        
if __name__ == '__main__':
    unittest.main()
