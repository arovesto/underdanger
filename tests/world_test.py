from src.game.world.board.board import create_board


def test_add(world, player):
    assert len(world.mobs) == 0
    world.add(player, (100, 121))
    assert len(world.mobs) == 1
    assert player.position == (100, 121)
    assert player.world == world
    assert world.mobs[(100, 121)] == player


def test_can_move(world, player):
    world.add(player, (0, 0))
    world.add_board(create_board([".#e"]), exits=None)

    assert not world.can_move(player, (-5, 1))
    assert not world.can_move(player, (15, 1))

    assert not world.can_move(player, (0, 1))
    assert world.can_move(player, (0, 2))


def test_create_player(world):
    world.add_board(create_board(["...", "...", "..."]), exits=None)

    p = world.create_player((0, 0), 'рыцарь', "Vasya")
    assert p.name == "Vasya"
    assert p.position == (0, 0)
    assert world.mobs[(0, 0)] == p

    assert p.world == world
    assert p.position == (0, 0)

    p2 = world.create_player((2, 2), 'рыцарь', "Petya")
    assert world.mobs[(0, 0)] == p
    assert world.mobs[(2, 2)] == p2


def test_is_occupied(lineworld):
    lineworld.create_warrior((0, 1))
    lineworld.create_archer((0, 2))
    lineworld.create_player((0, 3), 'рыцарь', "Vasya")
    assert not lineworld.is_occupied((0, 0))
    assert lineworld.is_occupied((0, 1))
    assert lineworld.is_occupied((0, 2))
    assert lineworld.is_occupied((0, 3))


def test_has_player_at(lineworld):
    assert lineworld.has_player_at((0, 0)) is not None
    assert not lineworld.has_player_at((0, 0))
    assert not lineworld.has_player_at((0, 1))

    lineworld.create_player((0, 0), 'рыцарь', "Vasya")
    assert lineworld.has_player_at((0, 0))
    assert not lineworld.has_player_at((0, 1))
