from src.geometry.direction import DIRS


class Action:
    def handle(self, game, *args):
        raise NotImplementedError("Should be implemented in subclasses")

    def can_perform(self, game, *args):
        raise NotImplementedError("Should be implemented in subclasses")


class Move(Action):
    def handle(self, game, *args):
        player = game.action_player
        target = DIRS[args[0]].go(player.position)
        if not self.can_perform(game, *args):
            if player.ap < player.points_to_go(target):
                return player.name + " не имеет достаточно очков чтобы туда походить"
            return player.name + "не может туда походить"
        player.move(target, player.points_to_go(target))
        return player.name + " походил"

    def can_perform(self, game, *args):
        player = game.action_player
        target = DIRS[args[0]].go(player.position)
        return game.world.can_move(player, target) and player.ap >= player.points_to_go(target)


class ActionHandler:
    actions = {}  # name - value shit

    def __init__(self, game):
        self.game = game

    def act(self, action_name, *args):
        action = self.actions.get(action_name, None)
        if action is None:
            return "Can't find such action, some error occurred"
        # Should be here something game-like, with part of the world, not with anything
        return action.handle(self.game, *args)

    def possible_actions(self):
        return [n for n, a in self.actions.items() if a.can_perform(self.game)]
