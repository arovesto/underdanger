import random

from data.res import names
from src.mobile.npc.npc import Npc
from src.util.drop_choise import probability_range
from src.equipment.items import small_heal_potion, normal_heal_potion
from src.equipment.armor import metal_mail, shoes, rogue_helmet, aluminium_mail, stealth_cloak
from src.equipment.weapons import metal_bow, metal_knife, better_archer_bow, spear
from src.equipment.items import standard_speed_potion, big_heal_potion, super_armor


class Merchant(Npc):
    see = 6
    max_ap = 6
    max_hp = 10

    def __init__(self):
        super().__init__('торговец', '$M')
        self.name = random.choice(names)
        self.ap = self.max_ap
        self.hp = self.max_hp

    def start_equip(self):
        self.drop = probability_range({})
        self.store = self.store_dict([(10, small_heal_potion()), (15, normal_heal_potion()),
                                      (50, metal_mail()), (30, shoes()), (100, metal_bow()), (50, rogue_helmet()),
                                      (50, standard_speed_potion()), (20, big_heal_potion()), (200, aluminium_mail()),
                                      (100, metal_knife()), (100, better_archer_bow()), (200, stealth_cloak()),
                                      (50, spear()),
                                      (200, super_armor())])
        return self

    def mech(self):
        self.do_random_move()

    def sold(self, customer, item_name):
        customer.money -= self.store[item_name].price
        customer.inventory.append(self.store[item_name])
        return '{} покупает {} за {}'.format(customer.name, item_name, self.store[item_name].price)

    def store_dict(self, items_):
        chosen = []
        items = [a for a in items_]
        elements_number = (len(items) * 3 + random.randint(-len(items), len(items))) // 4
        for _ in range(elements_number):
            choice = random.choice(items)
            chosen.append(choice)
            items.remove(choice)

        result_dict = {}
        for price, item in chosen:
            item.price = random.randrange(price - (price // 10), price + (price // 10) + 1)
            result_dict[item.name] = item
        return result_dict

    def show_items(self):
        return self.kind + ' продает:\n' + '\n'.join(str(item)
                                                     for item in list(self.store.values()))

    def get_trade_info(self):
        return dict(trader_name=self.name, trader_type=self.kind, trades=[e.info() for e in sorted(self.store.values(), key=lambda x: x.name)])