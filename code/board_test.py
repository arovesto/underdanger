import random

from board import BoardGenerator, create_board, create_figure, Rectangle, rotate
from square import Square


def test_is_inside():
    r = Rectangle((3, 5))

    assert r.is_inside((0, 0))
    assert r.is_inside((1, 1))
    assert r.is_inside((2, 2))
    assert r.is_inside((2, 3))
    assert r.is_inside((2, 4))
    assert r.is_inside((0, 4))
    assert r.is_inside((2, 0))

    assert not r.is_inside((-3, -8))
    assert not r.is_inside((-3, 8))
    assert not r.is_inside((-1, 0))
    assert not r.is_inside((0, -1))
    assert not r.is_inside((3, 3))
    assert not r.is_inside((2, 5))
    assert not r.is_inside((3, 5))


def test_neighbours():
    r = Rectangle((2, 2))
    assert r.neighbours((0, 0)) == [(0, 1), (1, 0), (1, 1)]


def test_rotate_right():
    model = create_figure(['...', '.#.', '.#.'])
    rotated = rotate(create_figure(['...', '.##', '...']))
    assert model == rotated


def test_generate():
    random.seed(10)
    b = BoardGenerator((10, 10)).generate()

    squares = [b.square((i, j)) for i in range(10) for j in range(10)]
    floor_count = len([s for s in squares if s.kind == 'floor'])
    wall_count = len([s for s in squares if s.kind == 'wall'])
    grass_count = len([s for s in squares if s.kind == 'grass'])

    assert floor_count > 0
    assert wall_count > 0
    assert grass_count > 0


def test_create_board():
    lines = ["###",
             "#..",
             "#.#"]
    b = create_board(lines)
    assert b.square((0, 0)).kind == 'wall'
    assert b.square((0, 1)).kind == 'wall'
    assert b.square((0, 2)).kind == 'wall'
    assert b.square((1, 0)).kind == 'wall'
    assert b.square((1, 1)).kind == 'floor'
    assert b.square((1, 2)).kind == 'floor'
    assert b.square((2, 0)).kind == 'wall'
    assert b.square((2, 1)).kind == 'floor'
    assert b.square((2, 2)).kind == 'wall'


def test_create_figure():
    lines = ["###",
             "#..",
             "#.#"]
    f = create_figure(lines)
    assert f[(0, 0)].kind == 'wall'
    assert f[(0, 1)].kind == 'wall'
    assert f[(0, 2)].kind == 'wall'
    assert f[(1, 0)].kind == 'wall'
    assert f[(1, 1)].kind == 'floor'
    assert f[(1, 2)].kind == 'floor'
    assert f[(2, 0)].kind == 'wall'
    assert f[(2, 1)].kind == 'floor'
    assert f[(2, 2)].kind == 'wall'


def test_add_figure():
    g = BoardGenerator((11, 11))
    f = {(0, 0) : Square('wall'),
         (0, 1) : Square('floor'),
         (0, -2) : Square('water'),
         (0, -10) : Square('grass')}

    g.add_figure((5, 5), f)
    b = g.create_board()

    assert b.square((5, 5)).kind == 'wall'
    assert b.square((5, 6)).kind == 'floor'
    assert b.square((5, 3)).kind == 'water'

    assert (5, -5) not in b.squares


def test_add_figure_no_override():
    g = BoardGenerator((3, 3))
    f = {(0, 0) : Square('wall'), (0, 1) : Square('floor')}

    g.add_figure((0, 0), f)
    b1 = g.create_board()
    assert b1.square((0, 0)).kind == 'wall'
    assert b1.square((0, 1)).kind == 'floor'

    g.add_figure((0, 1), f, override = False)
    b2 = g.create_board()
    assert b2.square((0, 1)).kind == 'floor'

    g.add_figure((0, 1), f, override = True)
    b3 = g.create_board()
    assert b3.square((0, 1)).kind == 'wall'
