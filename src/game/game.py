from src.game.world.world import World
from src.game.world.board.board import generate_game_board
from data.res import win_words, small_controls

from src.geometry.geometry import square, merge


class Game:
    def __init__(self, names, classes, shape):
        assert len(names) > 0, 'You can use only positive number of players'
        self.moves_counter = 0
        self.log = ''
        self.who_action = 'игрок'
        self.name_act_player = names[0]

        self.names = names
        self.shape = shape
        self.treat_radius = 9
        self.mobs_moving_times = 1

        board, start_position, exit_position = generate_game_board(shape)
        self.world = World()
        self.world.add_board(board, exit_position)
        self.world.add_players(names, classes, start_position)
        self.world.place_npcs()

        # FIXME add transaction classes for better logging and work
        self.action_player = next(p for p in self.world.players.values() if p.name == self.name_act_player)

    def run_checks(self):
        self.log += self.action_player.level_up()
        self.remove_dead_players()
        if self.world.can_heal_players(self.treat_radius):
            for p in self.world.mobs.values():
                if p.kind == 'игрок': p.heal()
            self.log += '\nВаше здоровье было восстановлено.'

        if self.action_player.ap <= 0:
            self.action_player.rest()
            self.who_action = 'mobs'
            self.name_act_player = self.names[(self.names.index(self.name_act_player) + 1) % len(self.names)]
            self.log += '\n' + self.action_player.name + ' кончилась энергия, ход переходит к ' + self.name_act_player
            self.action_player = next(p for p in self.world.players.values()
                                      if p.name == self.name_act_player)

        if self.who_action == 'игрок' and self.action_player.name == self.names[
            0] and self.action_player.ap == self.action_player.max_ap:
            self.moves_counter += 1
            self.log += '\nНачался новый ход'

    def run_action(self, action):
        self.log = ''
        act, *args = action
        if action != 'Not command':
            if action == "controls":
                self.log += "\n" + self.controls()
                return
            start_ap = self.action_player.ap
            getattr(self.action_player, act)(*args)
            end_ap = self.action_player.ap
            self.log += '\n' + self.action_player.last_happend
            if start_ap > end_ap: self.who_action = 'mobs'
        self.log += self.action_player.pick_up_item()

    def run_mech(self):
        # FIXME what the fuck even here, looks like metch is work for 2 times at first and one times after, i dunno
        not_player_characters = [m for m in self.world.mobs_near(merge([square(pos, self.treat_radius * 2)
                                                                        for pos in self.world.players])).values() if
                                 m.kind != 'игрок']
        for _ in range(self.mobs_moving_times):
            for mob in not_player_characters:
                if mob.ap <= 0:
                    mob.rest()
                    continue
                mob.last_happend = ''
                if self.game_over():
                    return
                mob.mech()
                self.log += mob.last_happend
        self.who_action = 'игрок'

    def make_statistics(self):
        for p in self.world.players.values():
            self.log += '\n' + p.name + '\nТы убил: {}'.format(p.kill_count)
        self.log += " Отличная работа:)"

    def game_over(self):
        pls_pos = list(self.world.players)
        if len(pls_pos) == 0:
            self.log += '\nВсе умерли, игра окончилась'
            return True
        if any(self.world.is_exit(p) for p in pls_pos):
            self.log = win_words
            return True
        return False

    def remove_dead_players(self):
        for name in self.names:
            if 'убил игрока ' + name in self.log:
                self.name_act_player = self.names[(self.names.index(self.name_act_player) + 1) % len(self.names)]
                self.action_player = next(p for p in self.world.players.values() if p.name == self.name_act_player)
                self.names.remove(name)

    def plot(self):
        return self.action_player.plot()

    def controls(self):
        return small_controls

    def remove_player(self, name):
        self.names.remove(name)
        self.world.remove_player(name)
        if self.name_act_player == name:
            self.name_act_player = self.names[(self.names.index(self.name_act_player) + 1) % len(self.names)]
            self.action_player = next(p for p in self.world.players.values() if p.name == self.name_act_player)

    def player_see(self, name):
        player = None
        for p in self.world.players.values():
            if p.name == name:
                player = p
                break
        visual = player.plot().strip("\n ").replace("\n", "<br/>")
        stats_visual = [p.stats().replace("\n", "<br/>") for p in self.world.players.values()]
        return dict(
            visual=visual,
            stats_visual=stats_visual,
            last_happened=player.last_happend,
            log=self.log,
            is_active=self.name_act_player == player.name,
            name=player.name,
            money=player.money,
            see_radius=player.see,
            ap=player.ap,
            hp=player.hp,
            max_ap=player.max_ap,
            max_hp=player.max_hp,
            exp=player.exp,
            next_level_exp=player.next_level_exp,
            level=player.level,
            inventory=[i.info() for i in player.inventory],
            magicbook=[i.info() for i in player.magicbook],
            equipment={part: i.info() if i is not None else None for part, i in player.equipment.items()}
        )
