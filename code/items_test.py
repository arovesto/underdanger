from player import Player
from items import rest_potion


def test_APRestorePotion():
    p = Player("Vasyan")
    p.inventory.append(rest_potion())
    p.ap = 3
    p.max_ap = 10
    assert p.ap != p.max_ap
    p.use(rest_potion().name)
    assert p.ap == p.max_ap
