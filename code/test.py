import unittest

from archer_test import ArcherTest
from board_test import BoardTest
from direction_test import DirectionTest
from game_test import GameTest
from geometry_test import GeometryTest
from player_test import PlayerTest
from world_test import WorldTest
from items_test import ItemsTest
from merchant_test import MerchantTest
from mobile_object_test import MobileObjectTest

tests = [ArcherTest, BoardTest, DirectionTest, MobileObjectTest, GameTest, GeometryTest, PlayerTest, WorldTest, ItemsTest, MerchantTest]
loader = unittest.defaultTestLoader

suite = unittest.TestSuite(loader.loadTestsFromTestCase(t) for t in tests)

runner = unittest.TextTestRunner(verbosity = 2)
runner.run(suite)
