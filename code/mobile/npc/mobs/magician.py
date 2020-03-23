import random

from code.mobile.npc.mobs.merchant import Merchant
from code.util.drop_choise import probability_range
from code.equipment.items import small_heal_potion, normal_heal_potion, big_heal_potion, big_speed_potion, new_map, \
    undying, \
    scroll_of_blindness, scroll_of_sleeppy
from code.equipment.armor import magic_tunic
from code.geometry.direction import DIRS


class Magician(Merchant):
    def __init__(self):
        super().__init__()
        self.kind = "странник"
        self.look = "*M"
        self.max_ap = 2
        self.direction_preference = [d for d in DIRS.values()]
        random.shuffle(self.direction_preference)

    def start_equip(self):
        # TODO cooler staff like scrolls (already here) + random layaout and prices
        self.drop = probability_range({})
        self.store = self.store_dict([(8, small_heal_potion()), (12, normal_heal_potion()), (16, big_heal_potion()),
                                      (60, big_speed_potion()), (300, new_map()), (100, undying()),
                                      (200, scroll_of_blindness()),
                                      (250, magic_tunic()), (100, scroll_of_sleeppy())])
        return self

    def mech(self):
        if self.find_player():
            return self.do_random_move()
        where_to_go = next((d for d in self.direction_preference if self.world.can_move(self, d.go(self.position))),
                           None)
        if where_to_go and self.ap > 0:
            return self.do_move(where_to_go.go(self.position))
        return self.rest()
