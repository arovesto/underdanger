import random

from data.res import names
from code.geometry.direction import DIRS
from code.mobile.npc.npc import Npc
from code.equipment.weapons import warrior_knife, better_warrior_knife
from code.equipment.items import rest_potion, standard_speed_potion, glasses, money_bag
from code.util.drop_choise import probability_range


class Warrior(Npc):
    see = 10
    max_hp = 15
    max_ap = 4
    points_to_attack = 2
    awareness = 1.0

    def __init__(self):
        super().__init__('мечник', '!W')
        self.name = random.choice(names)
        self.die_exp = 1
        self.hp = self.max_hp
        self.ap = self.max_ap
        self.knife = warrior_knife().equip(self)

    def start_equip(self):
        self.drop = probability_range({0.1: rest_potion(), 0.2: glasses(),
                                       0.05: standard_speed_potion(), 0.5: money_bag()(random.randrange(15, 20))})
        return self

    def find_direction_on_player(self):
        for direction in DIRS.values():
            if self.world.has_player_at(direction.go(self.position)):
                return direction

    def mech(self):
        # TODO polish things here (find-lose system)

        if self.state == 'observe':
            self.find_player()
            self.awareness += 0.04
        elif self.state == 'attack' and not self.lose_player():
            self.call_for_help(self.player)
            direction = self.find_direction_on_player()
            if self.ap >= self.points_to_attack and direction:
                self.last_happend = '\n' + self.show() + self.knife.use(direction)
            else:
                positions = [d.go(self.player.position) for d in DIRS.values()]
                if positions:
                    self.do_move_to(positions)
                    self.last_happend = ''
                    # self.last_happend = '' #'\n' + self.show() + self.do_move_to(self.player.position)
                else:
                    self.do_random_move()
                    self.last_happend = ''
        else:
            self.ap = 0

    def level_up(self):
        self.level += 1
        self.max_hp += 2
        if self.level < 6: self.see += 1
        if self.level % 3 == 0: self.die_exp += 1
        if self.level % 2 == 0: self.max_ap += 1
        if self.level == 3: self.knife = better_warrior_knife().equip(self)
