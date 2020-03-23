from game import Game
from direction import RIGHT


def test_run_action():
    g = Game(names=['Vasya'], classes=['рыцарь'], shape=(25, 25))
    p = g.action_player
    pos = p.position
    assert p.ap == p.max_ap

    g.run_action(['move_player', 'right'])

    assert p.position == RIGHT.go(pos)
    assert p.ap == p.max_ap - 1
