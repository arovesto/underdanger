from code.mobile.mobile_object import MobileObject


def test_can_see():
    m = MobileObject()
    m.see = 10
    m.position = (0, 0)
    assert not m.can_see((-100, 20))
    assert m.can_see((-4, 4))
