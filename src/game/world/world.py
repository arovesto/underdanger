import random
from typing import Dict, Tuple

from src.mobile.npc.mobs.warrior import Warrior
from src.mobile.npc.mobs.archer import Archer
from src.mobile.npc.mobs.merchant import Merchant
from src.mobile.npc.mobs.magician import Magician
from src.geometry.geometry import distance
from src.mobile.npc.player.classes import generate_player
from data.res import list_of_mobs, bad_mobs, opaque, npc
from src.mobile.npc.player.player import Player
from data.res import walkable_for_players

class World:
    def __init__(self):
        self.mobs = {}
        self.players: Dict[Tuple[int, int], Player] = {}
        self.drop = {}
        self.mob_level = 1
        self.exits = []
        self.board = None

    def add_board(self, board, exits):
        self.board = board
        self.exits = exits

    def is_exit(self, position):
        return position in self.exits

    def add_players(self, names, classes, position):
        pos = position
        if not self.can_move_player(pos):
            pos = next(p for p in self.board.neighbours(position) if self.can_move_player(p))
        for name, class_ in zip(names, classes):
            player = self.create_player(pos, class_, name)
            pos = next(p for p in self.board.neighbours(position) if self.can_move(player, p))

    def random_empty_position(self):
        position = self.board.random_position()
        if not self.is_occupied(position) and self.board.square(position).can_place_npc_here():
            return position
        else:
            return self.random_empty_position()

    def place_npcs(self, density=0.03):
        mob_count = int(density * self.board.area)
        for _ in range(mob_count):
            create = getattr(self, 'create_' + random.choice(list_of_mobs))
            create(self.random_empty_position())

    def place_drop(self, item, position):
        if position in self.drop:
            self.drop[position].append(item)
        else:
            self.drop[position] = [item]

    def add(self, entity, position):
        entity.position = position
        entity.world = self
        self.mobs[position] = entity
        return entity

    def create_warrior(self, position):
        warrior = Warrior().start_equip()
        return self.add(warrior, position)

    def create_magician(self, position):
        magician = Magician().start_equip()
        return self.add(magician, position)

    def create_archer(self, position):
        archer = Archer().start_equip()
        return self.add(archer, position)

    def create_merchant(self, position):
        merchant = Merchant().start_equip()
        return self.add(merchant, position)

    def create_player(self, position, class_, name):
        player = generate_player(class_, name)
        self.players[position] = player
        return self.add(player, position)

    def is_drop(self, position):
        return position in self.drop

    def items_names(self, positions):
        return ', '.join(d.name for p in positions for d in self.drop[p])

    def is_occupied(self, position):
        return position in self.mobs

    def can_move(self, entity, position):
        return (self.board.is_inside(position) and self.board.square(position).kind in entity.walkable_objects
                and not self.is_occupied(position))

    def can_move_player(self, position):
        return (self.board.is_inside(position) and self.board.square(position).kind in walkable_for_players
                and not self.is_occupied(position))

    def mobs_near(self, shape):
        # Not optimized, yet called only once
        return {pos: self.mobs[pos] for pos in shape if pos in self.mobs}

    def all_map(self):
        plotted = ''
        for i in range(self.board.shape[0]):
            line = ''
            for j in range(self.board.shape[1]):
                if self.is_occupied((i, j)):
                    line += self.mobs[(i, j)].look
                elif self.board.is_inside((i, j)):
                    line += self.board.square((i, j)).look
            plotted += ('\n' + line)
        return plotted

    def if_square_is(self, position, possibles):
        return position in self.board.squares and self.board.squares[position].kind in possibles

    def if_mob_is(self, position, possibles):
        # FIXME not optimized for in-square only
        return position in self.mobs and self.mobs[position].kind in possibles

    def square_kind(self, position):
        return self.board.square(position).kind

    def square_cost(self, position):
        return self.board.square(position).points_to_go

    def if_wall(self, position):
        return self.if_square_is(position, opaque)

    def has_player_at(self, position):
        # FIXME done?
        # return position in self.mobs and self.mobs[position].kind == 'игрок'
        return position in self.players

    def can_heal_players(self, treat_radius, mobs=None):
        # FIXME done?
        if not mobs:
            mobs = self.mobs
        return all(distance(m, p) > treat_radius for p in self.players
                   for m in mobs if mobs[m].kind in bad_mobs) and any(p.hp < p.max_hp for p in self.players.values())

    def power_up_monsters(self):
        # FIXME not optimized for in-square only
        for m in self.mobs.values():
            if m.kind in npc: m.level_up()
        # Use lazy computations, add set-level to npcs, and set it to the needed level as loaded
        self.mob_level += 1

    def nearest_exit_to(self, position):
        return min(self.exits, key=lambda x: distance(x, position))

    def remove_player(self, name):
        for (pos, p) in self.players.items():
            if p.name == name:
                del self.players[pos]
                del self.mobs[pos]
                return
