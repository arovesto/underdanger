import random

from res import names, not_flyable, walkable_for_monsters
from direction import DIRS, anti_dir
from npc import Npc
from weapons import archer_bow, better_archer_bow
from items import small_heal_potion, glasses, money_bag, bag, big_heal_potion
from drop_choise import probability_range
from geometry import distance

class Archer(Npc):
    see = 12
    max_hp = 8
    max_ap = 4
    move_penalty = 1
    awareness = 1.0
    
    def __init__(self):
        super().__init__('лучник', '{A')
        self.name = random.choice(names)
        self.hp = self.max_hp
        self.ap = self.max_ap
        self.die_exp = 2
        self.bow = archer_bow().equip(self)

    def start_equip(self):
        self.drop = probability_range({0.1 : small_heal_potion(), 0.2 : glasses(), 0.5 : money_bag()(random.randrange(5, 15)),
            0.101 : bag()(money_bag()(random.randrange(25, 35)), glasses(), big_heal_potion(), archer_bow(), name = 'сумка лучника')})
        return self
    
    def find_direction_on_player(self):
        for direction in DIRS.values():
            p = self.position
            for _ in self.bow.range:
                p = direction.go(p)
                if self.world.has_player_at(p):
                    return direction
                elif self.world.if_square_is(p, not_flyable):
                    break
        
    def mech(self):
        # TODO polish things here (find-lose system)
        if self.state == 'observe':
            self.find_player()
            self.awareness += 0.04
        elif self.state == 'attack' and not self.lose_player():
            self.call_for_help(self.player)
            direction_on_target = self.find_direction_on_player()
            if self.ap >= self.bow.cost and direction_on_target:
                self.last_happend = '\n' + self.show() + self.bow.use(direction_on_target)
            elif direction_on_target:
                self.do_move_to([anti_dir(direction_on_target).go(self.position)])
                self.last_happend = '\n' + self.show() + " отходит от игрока для выстрела"
            else:
                possible_position = []
                for direction in DIRS.values():
                    p = self.player.position
                    for _ in self.bow.range:
                        p = direction.go(p)
                        if self.world.if_square_is(p, walkable_for_monsters):
                            possible_position.append(p)
                        else:
                            break
                if len(possible_position) > 0:
                    self.last_happend = ''
                    self.do_move_to(possible_position)
                else:
                    self.last_happend = ''
                    self.do_move_to([self.player.position])
        else:
            self.ap = 0
    
    def level_up(self):
        self.level += 1
        self.max_hp += 1
        if self.level % 2 == 0: self.max_ap += 1
        if self.level % 3 == 0: self.die_exp += 1
        if self.level == 4: self.bow = better_archer_bow().equip(self)
        if self.level < 6: self.see += 1
        