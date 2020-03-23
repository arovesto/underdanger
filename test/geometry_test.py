from src.geometry.geometry import distance, add, manhattan, in_square, square, merge


def test_distance():
    assert distance((0, 0), (0, 3)) == 3
    assert distance((1, 1), (4, 5)) == 5


def test_add():
    assert add((-1, -1), (1, 1)) == (0, 0)
    assert add((20, -4), (0, 124)) == (20, 120)


def test_manhattan():
    assert manhattan((1, 0), (10, 0)) == 9
    assert manhattan((-1, -1), (7, 8)) == 17


def test_in_square():
    assert in_square((4, 4), (0, 0), 4)
    assert not in_square((5, 4), (0, 0), 4)
    assert not in_square((4, 5), (0, 0), 4)


def test_square():
    assert square((1, 1), 0) == [(1, 1)]
    assert set(square((1, 1), 1)) == {(1, 1), (0, 0), (2, 2), (1, 2), (2, 1), (0, 2), (2, 0), (1, 0), (0, 1)}


def test_merge():
    assert merge([square((1, 1), 1), square((2, 2), 1)]) == {(1, 1), (0, 0), (2, 2), (1, 2), (2, 1), (0, 2), (2, 0),
                                                             (1, 0), (0, 1), (2, 3), (3, 2), (3, 3),
                                                             (3, 1), (1, 3)}
