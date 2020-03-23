from src.geometry.direction import UP


def test_go():
    p = (2, 3)
    q = UP.go(p)
    assert q == (1, 3)
