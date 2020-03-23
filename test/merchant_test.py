import random

from src.mobile.npc.mobs.merchant import Merchant
from src.mobile.npc.player.player import Player
from src.equipment.items import normal_heal_potion


def test_show_items():
    m = Merchant().start_equip()
    assert m.show_items()[0:16] == 'торговец продает'


def test_sold(player):
    random.seed(44)
    m = Merchant().start_equip()
    c = m.sold(player, 'обычное восстановление')
    assert player.inventory[0].name == normal_heal_potion().name
    assert c[:-3] == player.name + ' покупает обычное восстановление за'
