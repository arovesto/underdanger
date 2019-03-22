import random 
import time
import tkinter as tk

from game import Game
from ui import get_stat_line
from acii_arts import  skull

from key_input import get_key

start_wors = '''
Greatings in DangerDangeon. This game is about exploring underground.
To win you need find exit(TT) and go through it. 
Enemies, like warrior(!W) and archer({A) will attack you.
You can trade with merchant($M), to buy staff.
Press "/" in game to see controls and info about your character.
You have HP or hit points. You lose it, when enemyes attack you.
When you lose all your HP game ends, and you lose.
If you kill all enemyes on map your helth will restore.
You have AP as action points. You can spend it on moving, or
attack, or shooting. All mobs have HP and AP too.
You can find information about how much AP you need to do something
if you press "/".
Press any enter to continue
'''
                                     
controls = '''
Use arrows to move.
Use enter + arrows to shoot.
Use l + arrows to attack.
Use space to spend one AP point.
Use / to see conrols.
Use esc to stop game.
'''


#Создание имён игроков
def read_player_names(number_of_players):
    print('Enter yours names, please')
    return [input('Your name: ') for n in range(number_of_players)]

def get_number_of_players():
    try:
        number_of_players = int(input('Number of players: '))
        return number_of_players
    except:
        print('It is not a number')
        return get_number_of_players()

def get_players_info():
    return read_player_names(get_number_of_players())

def get_action(player):
    print(player.name + ', what you want to do')
    print('You can do:', player.possible_commands)
    #action = input()
    action = get_key()
    if action in player.possible_keys:
        return action
    elif action == 'stop':
        print('Game was stoped')
        return 
    elif action == 'show description':
        print(player.info)
        print(controls)
        time.sleep(3)
        return 'Not command'
    else:
        print('Don`t understand, what you want, say again, please')
        time.sleep(1)
        return 'Not command'

def start_of_game():
    print(start_wors)
    input()
    
def show_happends(game, r):
    r.delete('0.0', 'end')
    r.insert('0.0', get_stat_line(game.world.mobs.values()))
    r.insert('0.0', game.log)
    r.insert('0.0', game.action_player.plot())

def end_of_game(game):
    if 'dies' in game.log:
        print('\f', skull)
            
def run_random_game(map_size=(10, 10)):
    start_coord = (random.randrange(3, map_size[0]-3), random.randrange(3, map_size[1]-3))
    end_coord = (random.randrange(3, map_size[0]-3), random.randrange(3, map_size[1]-3))
    
    #start_of_game()
    #names = get_players_info()
    names = ["Vasya", "Petya"]
    
    game = Game(names, map_size, start_coord, end_coord)
    
    root = tk.Tk()
    root.maxsize(width=1000, height=1000)
    root.resizable(width=False, height=False)
    text = tk.Text(root, height = 30, width = 68, bg="lightblue")
    text.pack()
    
    while not game.game_over():
        game.run_checks()
        show_happends(game, text)
        if game.who_action == 'игрок':
            action = get_action(game.action_player) 
            if action is None: return
            game.run_action(action)
        else:
            time.sleep(1)
            game.run_mech()
    
    end_of_game(game)        
    game.make_statistics()
    time.sleep(4)
    root.mainloop() 
    return

run_random_game(map_size=(100, 100))