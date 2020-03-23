from src.mobile.npc.mobs.archer import Archer
from src.geometry.direction import RIGHT
from src.game.world.world import World
from src.game.world.board.board import create_board


def test_find_direction_on_player():
    w = World()
    a = Archer()
    w.add(a, (0, 0))
    w.add_board(create_board(['...........', '..']), exits=None)
    assert a.find_direction_on_player() is None

    w.create_player((1, 1), 'рыцарь', "Vasya is on diagonal")
    assert a.find_direction_on_player() is None

    w.create_player((0, 20), 'рыцарь', "Vasya is too far")
    assert a.find_direction_on_player() is None

    w.create_player((0, 2), 'рыцарь', "Petya is near")
    assert a.find_direction_on_player() == RIGHT
