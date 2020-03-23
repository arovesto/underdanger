import random

from merchant import Merchant
from player import Player
from items import normal_heal_potion


def test_show_items():
    m = Merchant().start_equip()
    assert m.show_items()[0:16] == 'торговец продает'


def test_sold():
    random.seed(44)
    m = Merchant().start_equip()
    p = Player('Petyka')
    c = m.sold(p, 'обычное восстановление')
    assert p.inventory[0].name == normal_heal_potion().name
    assert c[:-3] == 'Petyka покупает обычное восстановление за'
