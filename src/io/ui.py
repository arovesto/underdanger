import os

from data.res import start_words, classes_info, classes
from src.util.acii_arts import skull


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_stat_line(mobs):
    return "\n".join([p.stats() for p in mobs])


def read_players_info(number_of_players):
    print('Введите свое имя, пожалуйста')
    names = []
    classes_ = []
    for i in range(number_of_players):
        class_, name = ask_player()
        names.append(name)
        classes_.append(class_)
    return names, classes_


def ask_player():
    name = input('Ваше имя? ')
    print(classes_info)
    class_ = input('Ваш класс? ')
    if class_ in classes:
        return class_, name
    else:
        print('Не существует класса {}'.format(class_))
        return ask_player()


def get_number_of_players():
    try:
        number_of_players = int(input('Сколько игроков будет? '))
        if number_of_players < 1:
            print("Слишком мало")
            return get_number_of_players()
        if number_of_players > 4:
            print("Слишком много")
            return get_number_of_players()
        return number_of_players
    except:
        print('Это не число')
        return get_number_of_players()


def start_of_game():
    print(start_words)
    input()


def show_happends(game):
    clear()
    print(game.plot())
    print(get_stat_line(game.world.players.values()))
    print(game.controls())
    print(game.log)
    print('\n')


def end_of_game(game):
    if 'умер' in game.log:
        clear()
        print("\n\n\n\nВы умерли. Игра окончена")
        print(skull)
    else:
        game.make_statistics()
        show_happends(game)


def get_players_info():
    return read_players_info(get_number_of_players())
