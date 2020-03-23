from src.game.world.board.board import create_board
from src.mobile.npc.player.player import Player
from src.game.world.world import World


def test_add():
    w = World()
    p = Player('Petrovich')
    assert len(w.mobs) == 0
    w.add(p, (100, 121))
    assert len(w.mobs) == 1
    assert p.position == (100, 121)
    assert p.world == w
    assert w.mobs[(100, 121)] == p


def test_can_move():
    w = World()
    p = Player('Petr')
    w.add(p, (0, 0))
    w.add_board(create_board([".#e"]), exits=None)

    assert not w.can_move(p, (-5, 1))
    assert not w.can_move(p, (15, 1))

    assert not w.can_move(p, (0, 1))
    assert w.can_move(p, (0, 2))


def test_create_player():
    w = World()
    w.add_board(create_board(["...", "...", "..."]), exits=None)

    p = w.create_player((0, 0), 'рыцарь', "Vasya")
    assert p.name == "Vasya"
    assert p.position == (0, 0)
    assert w.mobs[(0, 0)] == p

    assert p.world == w
    assert p.position == (0, 0)

    p2 = w.create_player((2, 2), 'рыцарь', "Petya")
    assert w.mobs[(0, 0)] == p
    assert w.mobs[(2, 2)] == p2


def test_is_occupied():
    w = World()
    w.add_board(create_board(["...."]), exits=None)

    w.create_warrior((0, 1))
    w.create_archer((0, 2))
    w.create_player((0, 3), 'рыцарь', "Vasya")
    assert not w.is_occupied((0, 0))
    assert w.is_occupied((0, 1))
    assert w.is_occupied((0, 2))
    assert w.is_occupied((0, 3))


def test_has_player_at():
    w = World()
    w.add_board(create_board(["...."]), exits=None)

    assert w.has_player_at((0, 0)) is not None
    assert not w.has_player_at((0, 0))
    assert not w.has_player_at((0, 1))

    w.create_player((0, 0), 'рыцарь', "Vasya")
    assert w.has_player_at((0, 0))
    assert not w.has_player_at((0, 1))
