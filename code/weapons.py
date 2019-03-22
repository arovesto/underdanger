from equipment import Equipment
from res import not_flyable, proper_warrior
from direction import DIRS, anti_dir
from geometry import distance

class Weapon(Equipment):
    kind = 'weapon'
    pass    

class Knife(Weapon):
    bodyparts = ['mainhand']
    look = '!.'
    
    def __init__(self, name = 'knife', damage = 4, cost = 2):
        self.damage = damage
        self.cost = cost
        self.name = name
        self.description = "Простой {}, бьет на {} за {} очков хода".format(name, damage, cost)
        
    def use(self, direction):
        p = direction.go(self.user.position)
        self.user.ap -= self.cost
        if self.user.world.if_mob_is(p, self.user.opponents):
            mob = self.user.world.mobs[p]
            return self.user.hit(mob, self)
        return ' ударил вникуда'

class Spear(Weapon):
    bodyparts = ["mainhand"]
    look = "./"

    def __init__(self, name = "копье", damage=6, cost=2, range_=3):
        self.damage = damage
        self.range = range_
        self.cost = cost
        self.name = name
        self.description = "Копье бьет на {} клеток нанося {} за {} очков. То что надо рыцарю".format(range_, damage, cost)

    def equip(self, user):
        self.user = user
        for part in self.bodyparts:
            self.user.equipment[part] = self
        if self.user.class_ in proper_warrior:
            self.damage += 2
            self.range += 1
        return self

    def unequip(self):
        for part in self.bodyparts:
            self.user.equipment[part] = None
        self.user.inventory.append(self)
        if self.user.class_ in proper_warrior:
            self.damage -= 2
            self.range -= 1

    def use(self, direction):
        p = self.user.position
        self.user.ap -= self.cost
        local_log = ''
        for _ in range(self.range):
            p = direction.go(p)
            if self.user.world.if_mob_is(p, self.user.opponents):
                mob = self.user.world.mobs[p]
                local_log += "\n" +  self.user.hit(mob, self)
        if len(local_log) == 0:
            return ' ударил вникуда'
        return local_log

class Bow(Weapon):
    bodyparts = ['mainhand', 'offhand']
    look = '{.'
    
    def __init__(self, name = 'bow', damage = 6, cost = 3, range_ = range(7)):
        self.name = name
        self.damage = damage
        self.cost = cost
        self.range = range_
        self.description = " стреляет на {} клеток за {} очков хода. Наносит {} урона".format(range_.stop, cost, damage)

    def use(self, direction):
        self.user.ap -= self.cost
        p = self.user.position
        for i in self.range:
            p = direction.go(p)
            if self.user.world.if_square_is(p, not_flyable):
                return " стрела застряла"
            elif self.user.world.if_mob_is(p, self.user.opponents):
                return self.user.hit(self.user.world.mobs[p], self)
        return ' стрела упала на землю'
        
class Whip(Weapon):
    bodyparts = ["offhand"]
    look = '(.'

    def __init__(self, name='хлыст', damage=5, cost=2, range_=3):
        self.name = name
        self.damage = damage
        self.cost = cost
        self.range_ = range_
        self.description = "Бьет вокруг на {} за {} очка".format(damage, cost)

    def use(self, direction):
        self.user.ap -= self.cost
        p = direction.go(self.user.position)
        dirs = {d for d in DIRS.values() if d != anti_dir(direction)}
        queue = [p]
        visited = set()
        log_message = ""
        # FIXME Something still wrong, one mob hit twice
        while len(queue) > 0:
            a = queue.pop(0)
            if a in visited:
                continue
            visited.add(a)
            if self.user.world.if_mob_is(a, self.user.opponents):
                log_message += "\n" + self.user.hit(self.user.world.mobs[a], self)
            queue.extend([d.go(a) for d in dirs if distance(d.go(a), self.user.position) <= self.range_ and d.go(a) not in visited])
        if len(log_message) == 0:
            return " никуда не попал хлыстом"
        return " своим хлыстом:" + log_message



    
def player_knife(): return Knife(damage = 8, cost = 2, name = 'меч')
def player_small_knife(): return Knife(damage = 3, cost = 1, name = 'нож')
def warrior_knife(): return Knife(damage = 4, cost = 2, name = 'тупой кинжал')
def better_warrior_knife(): return Knife(damage = 5, cost = 2, name = 'бронзовый кинжал')
def metal_knife(): return Knife(name = 'металлический кинжал', damage = 9, cost = 2)

def better_archer_bow(): return Bow(name = 'арбалет', damage = 7, cost = 3, range_ = range(15))
def player_bow(): return Bow(name = 'лук', damage = 7, cost = 3, range_ = range(10))
def archer_bow(): return Bow(damage = 4, cost = 2, range_ = range(10), name = 'малый лук')
def metal_bow(): return Bow(damage = 15, cost = 5, range_ = range(10), name= 'хороший лук')

def spear(): return Spear(name="копье",damage=6, cost=2, range_=2)

def whip(): return Whip(name="хлыст", damage=3, cost=2, range_=3)

SwordOfSaintPeter = Knife(name = 'супермеч', damage = 12, cost = 4)
BrutusDagger = Knife(name = 'мегакинжал', damage = 6, cost = 2)