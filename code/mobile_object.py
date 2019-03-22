from geometry import sub, distance

class MobileObject:
    see = 0
    exp = 0
    level = 1
    die_exp = 0
    kill_count = 0
    move_penalty = 0
    already_moved = False
    look = "?!"
    kind = "mob"

    def __init__(self, kind='mob', look=''):
        self.kind = kind
        self.look = look
        self.world = None
        self.last_happend = ''
        self.equipment = {'mainhand' : None, 'offhand' : None, 'legs' : None,
                          'head' : None, 'trunk' : None, 'hands' : None, 'foot' : None}
  
    def rest(self):
        self.ap = self.max_ap
        return '\n' + self.show() + ' отдыхает'
        
    def show(self):
        return '{} {}, HP = {}, AP = {}'.format(self.kind.capitalize(), self.name, str(self.hp), str(self.ap))
        
    def drop_award(self):
        return ''
        
    def blocked_damage(self, damage):
        return damage

    def can_see(self, position):
        return self.see >= distance(self.position, position)
        
    def in_view_side(self, b):
        start = self.position
        if not self.can_see(b):
            return False
        for delta in sub(self.position, b):
            for i, d in enumerate(delta):
                start[i] += d[i]
                if self.world.square_kind(start) == 'wall':
                    return False
        return True
    
    def damage(self, entity, damage):
        entity.hp -= entity.blocked_damage(damage)
        if entity.hp <= 0:
            self.state = 'observe'
            return entity.die(self)
        return ' поразил ' + entity.kind + ' на ' + str(entity.blocked_damage(damage))
        
    def hit(self, entity, weapon):
        if entity.blocked_damage(weapon.damage) <= 0:
            return " не может пробить защиту " + entity.kind
        else:
            return self.damage(entity, weapon.damage)
                
    def die(self, killer):
        del self.world.mobs[self.position]
        if self.kind == "игрок":
            del self.world.players[self.position]
        killer.kill_count += 1
        killer.exp += self.die_exp
        if self.kind == 'игрок': return " убил игрока {}. он оставил {}".format(self.name, self.drop_award())
        return ' убил {} {}. он оставил {}'.format(self.kind, self.name, self.drop_award())
        
    def points_to_go(self, position):
        return self.world.square_cost(position) + self.move_penalty
    
    def move(self, target, need_points):
        self.ap -= need_points
        del self.world.mobs[self.position]
        self.world.mobs[target] = self
        if self.kind == "игрок":
            del self.world.players[self.position]
            self.world.players[target] = self
        self.position = target

    def is_player(self):
        pass