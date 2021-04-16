import random

from src.mobile.mobile_object import MobileObject
from src.geometry.geometry import distance, square
from data.res import walkable_for_monsters
from src.mobile.pathfinder import path
from src.geometry.direction import DIRS


class Npc(MobileObject):
    opponents = ['игрок']

    def __init__(self, kind, look):
        super().__init__(kind, look)
        self.walkable_objects = walkable_for_monsters
        self.state = 'observe'
        self.awareness = 0.5
        self.player = None
        self.drop = None

    def drop_award(self):
        chosen = random.random()
        try:
            item = next(i for prob, i in self.drop.items() if prob[0] < chosen <= prob[1])
            self.world.drop[self.position] = item
            return item.name
        except StopIteration:
            return 'ничего'

    def level_up(self):
        pass

    def do_move(self, target):
        need_points = self.points_to_go(target)
        if self.ap >= need_points:
            self.move(target, need_points)
            return ' передвинулся к ' + self.world.square_kind(self.position)
        else:
            self.ap -= 1
            return ' не имеет очков на передвижение'

    def do_move_to(self, positions):
        path_ = path(self, positions)
        if len(path_) == 0:
            return self.do_random_move()
        return self.do_move(path_[0])

    def can_walk_to(self, position):
        if not self.world.can_move(self, position):
            return False
        path_ = path(self, [position])
        return len(path_) != 0 and all(self.world.can_move(self, a) for a in path_)

    def do_random_move(self):
        possibles = [d.go(self.position) for d in DIRS.values() if self.world.can_move(self, d.go(self.position))]
        if len(possibles) != 0:
            return self.do_move(random.choice(possibles))
        else:
            return " не может двигаться"

    def observable(self, entity):
        # TODO may be this is stupid
        return self.see * self.awareness >= distance(entity.position, self.position) * entity.masking()
        # тут труднее всего. Надо смотреть на расстояние, то что на игроке надето
        # и сравнивать со внутренними параметрами и беспокойством

    def can_see_player(self, player):
        return self.can_see(player.position) and self.observable(player)

    def lose_player(self):
        return random.randrange(int(self.see / 1.7 * self.player.obscurity)) > \
               self.see * self.awareness or not self.can_see_player(self.player)

    def activate(self, player):
        self.player = player
        self.state = 'attack'
        self.last_happend = '\n' + self.show() + ' обнаружил игрока ' + player.name

    def call_for_help(self, player):
        how_much = 0
        for m in self.world.mobs_near(square(self.position, self.see * 2 // 3)).values():
            if m.kind == self.kind and self.can_see(m.position) and m is not self:
                m.activate(player)
                how_much += 1
        if how_much > 0:
            self.last_happend += "\n" + self.show() + " позвал на помощь {} товарищей".format(how_much)

    def find_player(self):
        player = next((p for p in self.world.players.values() if self.can_see_player(p)), None)
        if player:
            self.activate(player)
            self.call_for_help(player)
            return player.position
        return None

    def is_player(self):
        return False
