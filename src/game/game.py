from src.game.world.world import World
from src.game.world.board.board import generate_game_board
from data.res import win_words, small_controls
from src.util.words import name_to_genitive

from src.geometry.geometry import square, merge


class Game:
    def __init__(self, names, classes, shape):
        assert len(names) > 0, 'You can use only positive number of players'
        self.moves_counter = 0
        self.log = ''
        self.who_action = 'игрок'
        self.active_player_name = names[0]

        self.players_names = names
        self.shape = shape
        self.treat_radius = 12
        self.mobs_moving_times = 1
        self.dead_players = set()

        board, self.start_position, exit_position = generate_game_board(shape)
        self.world = World()
        self.world.add_board(board, exit_position)
        self.world.add_players(names, classes, self.start_position)
        self.world.place_npcs()

        # FIXME add transaction classes for better logging and work
        self.active_player = next(p for p in self.world.players.values() if p.name == self.active_player_name)

    def run_checks(self):
        self.active_player.ap = 1000  # FIXME to test no ap
        self.log += self.active_player.level_up()
        self.remove_dead_players()
        if self.world.can_heal_players(self.treat_radius):
            for p in self.world.mobs.values():
                if p.kind == 'игрок': p.heal()
            self.log += '\nВаше здоровье было восстановлено.'

        if self.active_player.ap <= 0:
            self.active_player.rest()
            self.who_action = 'mobs'
            self.active_player_name = self.players_names[(self.players_names.index(self.active_player_name) + 1) % len(self.players_names)]
            self.log += '\n' + self.active_player.name + ' кончилась энергия, ход переходит к ' + self.active_player_name
            self.active_player = next(p for p in self.world.players.values()
                                      if p.name == self.active_player_name)

        if self.who_action == 'игрок' and self.active_player.name == self.players_names[
            0] and self.active_player.ap == self.active_player.max_ap:
            self.moves_counter += 1
            self.log += '\nНачался новый ход'

    def run_action(self, action):
        self.log = ''
        self.active_player.last_happend = ""
        act, *args = action
        if action != 'Not command':
            if action == "controls":
                self.log += "\n" + self.controls()
                return
            start_ap = self.active_player.ap
            getattr(self.active_player, act)(*args)
            end_ap = self.active_player.ap
            self.log += '\n' + self.active_player.last_happend
            if start_ap > end_ap: self.who_action = 'mobs'
        self.log += self.active_player.pick_up_item()

        self.active_player_name = self.players_names[
            (self.players_names.index(self.active_player_name) + 1) % len(self.players_names)]
        self.active_player = next(p for p in self.world.players.values()
                                  if p.name == self.active_player_name)

    def run_mech(self):
        # FIXME what the fuck even here, looks like metch is work for 2 times at first and one times after, i dunno
        not_player_characters = [m for m in self.world.mobs_near(merge([square(pos, self.treat_radius * 2)
                                                                        for pos in self.world.players])).values() if
                                 m.kind != 'игрок']
        for _ in range(self.mobs_moving_times):
            for mob in not_player_characters:
                mob.ap = 100  # FIXME to test "do action every time"
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

    def get_status(self):
        pls_pos = list(self.world.players)
        if len(pls_pos) == 0:
            return 'lose'
        if any(self.world.is_exit(p) for p in pls_pos):
            return 'win'
        return 'in_progress'

    def remove_dead_players(self):
        if len(self.world.players.values()) == 0:
            return
        new_player_names = []
        for name in self.players_names:
            if 'убил игрока ' + name_to_genitive(name) in self.log:
                self.dead_players.add(name)
                if name == self.active_player_name:
                    self.active_player_name = self.players_names[(self.players_names.index(self.active_player_name) + 1) % len(self.players_names)]
                    self.active_player = next(p for p in self.world.players.values() if p.name == self.active_player_name)
            else:
                new_player_names.append(name)
        self.players_names = new_player_names

    def plot(self):
        return self.active_player.plot()

    def controls(self):
        return small_controls

    def remove_player(self, name):
        if self.active_player_name == name:
            self.active_player_name = self.players_names[(self.players_names.index(self.active_player_name) + 1) % len(self.players_names)]
            self.active_player = next(p for p in self.world.players.values() if p.name == self.active_player_name)
        self.players_names.remove(name)
        self.world.remove_player(name)

    def add_player(self, name, class_):
        self.world.add_players([name], [class_], self.start_position)
        self.players_names.append(name)

    def player_see(self, name):
        player = None
        for p in self.world.players.values():
            if p.name == name:
                player = p
                break
        if player is None:
            player = self.active_player
        rendered_map, tile_descriptions = player.plot_for_web()
        stats_visual = [p.stats().replace("\n", "<br>") for p in sorted(self.world.players.values(), key=lambda x: x.name)]
        return dict(
            dead_players=list(sorted(self.dead_players)),
            tile_descriptions=tile_descriptions,
            visual=rendered_map,
            stats_visual=stats_visual,
            last_happened=player.last_happend,
            log=self.log.strip().replace('\n', '<br>'),
            is_active=self.active_player_name == player.name,
            players_names=self.players_names,
            active_player_name=self.active_player_name,
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
            inventory=player.inventory_for_web(),
            magicbook=[i.info() for i in player.magicbook],
            equipment=[dict(part=part, info=i.info()) if i is not None
                       else dict(part=part, info=None) for part, i in sorted(player.equipment.items(), key=lambda x: x[0])],
            trade_offers=player.get_trade_offers(),
        )
