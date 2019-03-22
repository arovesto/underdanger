import unittest

from mobile_object import MobileObject

class MobileObjectTest(unittest.TestCase):
    def test_can_see(self):
        m = MobileObject()
        m.see = 10
        m.position = (0, 0)
        self.assertFalse(m.can_see((-100, 20)))
        self.assertTrue(m.can_see((-4, 4)))
    
        
if __name__ == '__main__':
    unittest.main()
