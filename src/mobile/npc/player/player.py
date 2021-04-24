from math import ceil
from collections import Counter

from src.geometry.direction import DIRS, directions_on
from src.mobile.mobile_object import MobileObject
from data.res import walkable_for_players, npc, max_armor_value, traders
from src.geometry.geometry import distance, square, manhattan, ring


class Player(MobileObject):
    window_height = 21
    window_width = 31
    pickup_distance = 1
    talking_distance = 2
    max_hp = 0
    max_ap = 0
    class_ = "Никто"
    descr = "мистер Никто"
    see = 12
    opponents = npc

    def __init__(self, name):
        super().__init__('игрок', '@' + name[0])
        self.name = name
        self.money = 0
        self.see = 12
        self.possible_keys = ['move_player', 'nothing', 'open_inventory', 'use', 'remove',
                              'info', 'showshopitems', 'trade', 'share', 'equip',
                              'use_main_weapon', "use_second_weapon" 'unequip', 'magic']
        self.inventory = []
        self.magicbook = []
        self.walkable_objects = walkable_for_players
        self.last_happend = ""
        self.next_level_exp = int(self.level ** 1.5 * 2 + 10)

    def start_equip(self):
        pass

    def level_up(self):
        if self.exp < self.next_level_exp: return ''
        message = ""
        while self.exp >= self.next_level_exp:
            self.exp -= self.next_level_exp
            self.level += 1
            self.next_level_exp = int(self.level ** 1.5 * 2 + 10)
            self.max_hp += 1
            self.see += 1
            self.heal()
            if self.level % 4 == 0: self.max_ap += 1
            message = '\n{} теперь имеет {} уровень'.format(self.name, self.level)
            if self.level % 2 == 0:
                self.world.power_up_monsters()
                message += ", монстры так же увеличили свою силу"
        return message

    def stats(self):
        return '{name}, {_class}, уровень {level}:\n[HP = {hp}, AP = {ap}, Защита = {armor}]. Деньги = {money}, EXP = {exp}'.format(
            name=self.name, _class=self.class_, hp=self.hp,
            armor=sum(a.block for a in self.equipment.values() if a is not None and a.kind == 'armor'),
            ap=self.ap, money=self.money, level=self.level, exp=self.exp)

    def heal(self):
        self.hp = self.max_hp

    def info(self):
        self.last_happend = '{}. Необходимо {} опыта до нового уровня.\nНесет с собой {}'.format(self.descr,
                                                                                                 self.next_level_exp - self.exp,
                                                                                                 '\n'.join(
                                                                                                     str(i) for i in
                                                                                                     set(
                                                                                                         self.equipment.values())
                                                                                                     if i is not None))
        if len(self.magicbook) > 0:
            self.last_happend += '\nТак же знает следующие заклинания:\n' + '\n'.join(str(m) for m in self.magicbook)

    def share(self, player_name, item_name):
        try:
            player = next(p for p in self.world.players.values() if p.name == player_name)
            item = next(i for i in self.inventory if i.name == item_name)
            if distance(self.position, player.position) <= self.talking_distance:
                self.inventory.remove(item)
                player.inventory.append(item)
                self.last_happend = '{} передал {} в руки {}'.format(self.name, item_name, player_name)
            else:
                self.last_happend = '{} слишком далеко от {}'.format(self.name, player_name)
        except StopIteration:
            self.last_happend = "{} не может дать {} в руки {}".format(self.name, item_name, player_name)

    def move_player(self, direction):
        target = DIRS[direction].go(self.position)
        if not self.world.can_move(self, target) and self.world.is_occupied(target):
            self.use_main_weapon(direction)
            if "не имеет" in self.last_happend:
                self.use_second_weapon(direction)
            if "не имеет" in self.last_happend:
                self.last_happend = self.name + ' не может походить туда'
        elif not self.world.can_move(self, target):
            self.last_happend = self.name + ' не может походить туда'
        else:
            need_points = self.points_to_go(target)
            if self.ap >= need_points:
                self.move(target, need_points)
            else:
                self.last_happend = self.name + ' не имеет очков хода чтобы походить'

    def showshopitems(self):
        nearby_merchant_items = (self.world.mobs[m].show_items() for m in self.world.mobs_near(square(self.position, 2))
                                 if self.world.mobs[m].kind in traders)

        self.last_happend = next(
            nearby_merchant_items, self.name + ' спросил никого о торгах')

    def get_trade_offers(self):
        for m in self.world.mobs_near(square(self.position, 2)):
            if self.world.mobs[m].kind in traders:
                return self.world.mobs[m].get_trade_info()
        return None

    def trade(self, item_name, merchant_name=""):
        try:
            merchant = next(self.world.mobs[m] for m in self.world.mobs_near(square(self.position, 2)) if
                            self.world.mobs[m].kind in traders if merchant_name == "" or self.world.mobs[m].name == merchant_name)
            if item_name not in merchant.store:
                self.last_happend = "у торговца нет " + item_name
            elif self.money < merchant.store[item_name].price:
                self.last_happend = self.name + ' не имеет достаточно денег на ' + item_name
            else:
                self.last_happend = merchant.sold(self, item_name)
        except StopIteration:
            self.last_happend = self.name + ' попытался поторговаться с никем'

    def open_inventory(self):
        # FIXME here, use counter properly pls
        showed_dict = Counter(self.inventory)
        self.last_happend = 'Предметы:\n'
        self.last_happend += '\n'.join(
            '{} - {}, {} штук'.format(item.name, item.description, showed_dict[item]) for item in showed_dict)
        self.last_happend += '\n'

    def inventory_for_web(self):
        showed_dict = Counter(self.inventory)
        return [dict(count=cnt, **item.info()) for item, cnt in sorted(showed_dict.items(), key=lambda x: x[0].name)]

    def blocked_damage(self, damage):
        return ceil(damage * (1 - (sum(
            a.block for a in self.equipment.values() if a is not None and a.kind == 'armor') / max_armor_value)))

    def masking(self):
        return self.obscurity

    def on_position_left(self, x, y):
        pos = (int(x), int(y))
        if pos == self.position:
            return
        directions = directions_on(self.position, pos)
        for d in directions:
            self.move_player(d)
            if "не может походить туда" not in self.last_happend:
                break
        else:
            self.last_happend = self.name + " не может походить туда"

    def on_position_right(self, x, y):
        pos = (int(x), int(y))
        if pos == self.position:
            return
        dirs = directions_on(self.position, pos)
        if len(dirs) == 0:
            return
        direction = dirs[0]
        self.use_main_weapon(direction)
        if "не имеет" in self.last_happend:
            self.use_second_weapon(direction)
        if "не имеет" in self.last_happend:
            self.last_happend = self.name + " не иммеет оружия"

    def equip(self, item_name):
        try:
            weapon = next(i for i in self.inventory if i.name == item_name and i.tag == 'equipable')
            for part in weapon.bodyparts:
                if self.equipment[part] is not None: self.equipment[part].unequip()
            weapon.equip(self)
            self.inventory.remove(weapon)
            self.last_happend = '{} надел {}'.format(self.name, item_name)
        except StopIteration:
            self.last_happend = "{} не может надеть {}".format(self.name, item_name)

    def unequip(self, item_name):
        try:
            weapon = next(i for i in set(self.equipment.values()) if i is not None and i.name == item_name)
            weapon.unequip()
            self.last_happend = '{} снял {}'.format(self.name, item_name)
        except StopIteration:
            self.last_happend = '{} не имеет {}'.format(self.name, item_name)

    def use(self, item_name, *item_args):
        try:
            item = next(i for i in self.inventory if i.name == item_name and i.kind == 'usable')
            self.last_happend = item.use(self, *item_args)
        except StopIteration:
            self.last_happend = self.name + " не может использовать " + item_name

    def equip_or_use(self, item_name, *item_args):
        try:
            item = next(i for i in self.inventory if i.name == item_name and i.kind == 'usable')
            self.last_happend = item.use(self, *item_args)
        except StopIteration:
            self.equip(item_name)

    def remove(self, item_name):
        try:
            item = next(i for i in self.inventory if i.name == item_name)
            item.remove(self)
            self.last_happend = '{} выкинул {}'.format(self.name, item.name)
        except StopIteration:
            self.last_happend = '{} не имеет {}'.format(self.name, item_name)

    def nothing(self):
        self.last_happend = '{} пропускает ход'.format(self.name)
        self.ap -= 1

    def use_weapon(self, weapon, direction):
        d = DIRS[direction]
        if self.ap >= weapon.cost:
            self.last_happend = self.name + weapon.use(d)
        else:
            self.last_happend = self.name + ' не имеет достаточно очков для ' + weapon.name

    def use_main_weapon(self, direction):
        if self.equipment['основное'] is not None and self.equipment['основное'].kind == 'weapon':
            return self.use_weapon(self.equipment['основное'], direction)
        else:
            self.last_happend = self.name + ' не имеет основного оружия'

    def use_second_weapon(self, direction):
        if self.equipment['дополнительное'] is not None and self.equipment['дополнительное'].kind == 'weapon':
            return self.use_weapon(self.equipment['дополнительное'], direction)
        else:
            self.last_happend = self.name + ' не имеет запасного оружия'

    def magic(self, magic_name):
        try:
            self.last_happend = self.name + next(
                magic for magic in self.magicbook if magic is not None and magic.name == magic_name).use()
        except StopIteration:
            self.last_happend = self.name + ' не имеет ' + magic_name

    def drop_on_world(self, item_name):
        try:
            item = next(i for i in self.inventory if i.name == item_name)
        except StopIteration:
            self.last_happend = self.name + ' не имеет ' + item_name
        else:
            try:
                pos = next(p for p in ring(self.position, self.pickup_distance + 1, self.pickup_distance + 1) if
                           self.world.can_move(self, p))
                item.remove(self)
                self.world.place_drop(item, pos)
                self.last_happend = self.name + " выбросил " + item_name + " на землю"
            except StopIteration:
                self.last_happend = self.name + " не может выбросить предмет потому что вокруг все занято"

    def pick_up_item(self):
        positions = [position for position in self.world.drop
                     if manhattan(self.position, position) <= self.pickup_distance]

        pick_up_message = ('\n{} поднял {}'.format(self.name, self.world.items_names(positions))
                           if len(positions) > 0 else '')
        for position in positions:
            self.inventory.extend(self.world.drop[position])
            del self.world.drop[position]
        return pick_up_message

    def drop_award(self):
        for item in self.inventory:
            self.world.place_drop(item, self.position)
        return ", ".join(i.name for i in self.inventory)

    def plot(self):
        start_line = '\n╔' + '══' * self.window_width + '╗'
        end_line = '\n╚' + '══' * self.window_width + '╝'

        map_plotted = start_line
        for i in range(self.position[0] - self.window_height // 2, self.position[0] + self.window_height // 2 + 1):
            line = ''
            for j in range(self.position[1] - self.window_width // 2, self.position[1] + self.window_width // 2 + 1):
                if abs(distance(self.position, (i, j)) - self.see) <= 1:
                    line += '░░'
                elif distance(self.position, (i, j)) > self.see:
                    line += '▒▒'
                elif self.world.is_occupied((i, j)):
                    line += self.world.mobs[(i, j)].look
                elif self.world.is_drop((i, j)):
                    line += self.world.drop[(i, j)][-1].look
                elif self.world.board.is_inside((i, j)):
                    line += self.world.board.square((i, j)).look
                else:
                    line += '▓▓'
            map_plotted += '\n║' + line + '║'
        map_plotted += end_line
        return map_plotted

    def plot_for_web(self):
        start_line = '╔' + '══' * self.window_width + '╗'
        end_line = '<br>╚' + '══' * self.window_width + '╝'
        descriptions = {}

        map_plotted = start_line
        for i in range(self.position[0] - self.window_height // 2, self.position[0] + self.window_height // 2 + 1):
            line = ''
            for j in range(self.position[1] - self.window_width // 2, self.position[1] + self.window_width // 2 + 1):
                if abs(distance(self.position, (i, j)) - self.see) <= 1:
                    line += '░░'
                elif distance(self.position, (i, j)) > self.see:
                    line += '▒▒'
                elif self.world.is_occupied((i, j)):
                    tile_id = f"tile_{i}_{j}"
                    descriptions[tile_id] = self.world.mobs[(i, j)].show()
                    style = ""
                    if self.world.board.is_inside((i, j)):
                        style = self.world.board.square((i, j)).style
                    line += f"<span class='map_tile' id='{tile_id}' style='{style}'>{self.world.mobs[(i, j)].look}</span>"
                elif self.world.is_drop((i, j)):
                    tile_id = f"tile_{i}_{j}"
                    descriptions[tile_id] = str(self.world.drop[(i, j)][-1])
                    style = ""
                    if self.world.board.is_inside((i, j)):
                        style = self.world.board.square((i, j)).style
                    line += f"<span class='map_tile' id='{tile_id}' style='{style}'>{self.world.drop[(i, j)][-1].look}</span>"
                elif self.world.board.is_inside((i, j)):
                    tile_id = f"tile_{i}_{j}"
                    descriptions[tile_id] = self.world.board.square((i, j)).description
                    style = self.world.board.square((i, j)).style
                    line += f"<span class='map_tile' style='{style}' id='{tile_id}'>{self.world.board.square((i, j)).look}</span>"
                else:
                    line += '▓▓'
            map_plotted += '<br>║' + line + '║'
        map_plotted += end_line
        return map_plotted, descriptions

    def is_player(self):
        return True
