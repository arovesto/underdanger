from code.equipment.equipment import Equipment
from code.geometry.geometry import distance, circle


class Magic(Equipment):
    def equip(self, user):
        self.user = user
        return self

    def __str__(self):
        return self.name + " - " + self.description


class MagicBomb(Magic):
    kind = 'bomb'
    look = '**'

    def __init__(self, name='bomb', max_damage=8, cost=3, range_=10):
        self.name = name
        self.max_damage = max_damage
        self.cost = cost
        self.range = range_
        self.decrement = max_damage / range_
        self.description = "наносит урон в радиусе {}, с {} рядом".format(range_, max_damage)

    def use(self):
        self.user.ap -= self.cost
        local_log = " использовал волшебный взрыв"
        target_enemyes = [self.user.world.mobs[m] for m in
                          self.user.world.mobs_near(circle(self.user.position, self.range))
                          if self.user.world.mobs[m].kind in self.user.opponents]
        for m in target_enemyes:
            self.damage = int(self.max_damage - self.decrement * distance(m.position, self.user.position))
            local_log += '\nон' + self.user.hit(m, self)
        return local_log


class MagicRing(Magic):
    kind = 'ring'
    look = '00'

    def __init__(self, name='волшебное кольцо', cost=2, range_=5):
        self.name = name
        self.cost = cost
        self.range = range_
        self.description = "одурманивает противников"

    def use(self):
        self.user.ap -= self.cost
        for m in self.user.world.mobs_near(circle(self.user.position, self.range)):
            if self.user.world.mobs[m].kind in self.user.opponents:
                self.user.world.mobs[m].ap = 0
                self.user.world.mobs[m].state = 'observe'
                self.user.world.mobs[m].awareness = 1.0
        return " своим волшебным кольцом обескураживает противников"


class Blindness(Magic):
    kind = "blindness"
    look = '00'

    def __init__(self, name='ослепление', cost=3, range_=7, effect=3):
        self.name = name
        self.cost = cost
        self.range = range_
        self.effect = effect
        self.description = "ослепляет противников в радиусе {} за {}. Одноразовое.".format(range_, cost)

    def use(self):
        self.user.ap -= self.cost
        for m in self.user.world.mobs_near(circle(self.user.position, self.range)):
            if self.user.world.mobs[m].kind in self.user.opponents:
                self.user.world.mobs[m].see = self.effect
                self.user.world.mobs[m].state = 'observe'
        self.user.magicbook.remove(self)
        return " ослепил противников"


class Sleepy(Magic):
    kind = "sleepy"
    look = '00'

    def __init__(self, name='усыпление', cost=2, range_=3, usages=10, step=0.2):
        self.name = name
        self.cost = cost
        self.range = range_
        self.usages = usages
        self.step = step
        self.description = "уменьшает бдительность врагов вокруг. {} использований".format(self.usages)

    def use(self):
        self.user.ap -= self.cost
        for m in self.user.world.mobs_near(circle(self.user.position, self.range)):
            if self.user.world.mobs[m].kind in self.user.opponents and self.user.world.mobs[m].awareness >= self.step:
                self.user.world.mobs[m].awareness -= self.step
        self.usages -= 1
        if self.usages == 0:
            self.user.magicbook.remove(self)
        self.description = "уменьшает бдительность врагов вокруг. {} использований".format(self.usages)
        return " усыпил противников"


def blindness(cost=3, effect=2): return Blindness(name='ослепление', cost=cost, effect=effect)


def small_ring(range_=5): return MagicRing(name='кольцо', range_=range_)


def magic_bomb(): return MagicBomb(name='взрыв')


def sleeppy(step=0.2, usages=10): return Sleepy(name="усыпление", step=step, usages=usages)
