import time
import pickle
import os

from src.game.game import Game
from src.io.ui import show_happends, start_of_game, get_players_info, end_of_game, clear
from data.res import controls, positive
from src.io.key_input import input_command


def get_action(player):
    print(player.name + ', что ты хочешь сделать?')
    action = input_command(player.possible_keys)
    if action[0] == 'stop':
        last_ask = input('Вы действительно хотите выйти? ')
        if last_ask in positive:
            return
        return "Not command"
    elif action[0] == 'show controls':
        print(controls)
        print('Нажми любую клавишу чтобы продолжить')
        input()
        return 'Not command'
    else:
        return action


def write_map(game):
    with open('!карта.txt', 'w', encoding='utf-8') as file:
        file.write(game.world.all_map())


def save_game(game):
    with open("game.dump", "wb") as f:
        pickle.dump(game, f)


def load_game():
    with open("game.dump", "rb") as f:
        game = pickle.load(f, encoding="utf-8")
    return game


def create_game(shape):
    start_of_game()
    names, classes = get_players_info()
    return Game(names, classes, shape)


def is_save_file():
    return os.path.isfile(os.getcwd() + os.sep + "game.dump")


def menu_choice(shape):
    if not is_save_file():
        return create_game(shape)
    answer = input("Хотите загрузить игру?: ")
    if answer in positive:
        print("Загружаю")
        return load_game()
    clear()
    return create_game(shape)


def run_random_game(shape):
    game = menu_choice(shape)

    if "Читер" in game.names:
        write_map(game)
    while not game.game_over():
        game.run_checks()
        show_happends(game)
        if game.who_action == 'игрок':
            action = get_action(game.action_player)
            if action is None:
                print("Выхожу...")
                save_game(game)
                return
            game.run_action(action)
        else:
            game.run_mech()

    end_of_game(game)
    if is_save_file():
        os.remove("game.dump")
    else:
        time.sleep(3)
    return


run_random_game((500, 500))
