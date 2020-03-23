import pytest

from src.game.world.world import World
from src.game.world.board.board import create_board
from src.mobile.npc.player.player import Player


@pytest.fixture
def world():
    return World()


@pytest.fixture
def player():
    return Player("Vasiliy")


@pytest.fixture
def lineworld():
    world = World()
    world.add_board(create_board(["...."]), exits=None)
    return world
