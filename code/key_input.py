from msvcrt import getch

def key_pressed(allowed_keys):
    k = getch()
    key = ord(k)
    k = k.decode("cp1251")
    if key == 224:
        key = ord(getch())
        if key == 80: k = 'down'
        elif key == 72: k = 'up'
        elif key == 75: k = 'left'
        elif key == 77: k = 'right'
        elif key == 83: k = 'delete'
    elif key == 13: k = 'enter'
    elif key == 27: k = 'escape'
    elif key == 32: k = 'space'

    if k in allowed_keys:
        return k
    else:
        print("Не понял тебя")
        return key_pressed(allowed_keys)

def get_argument(argument):
    print(argument.get('descr', ''))
    if argument['type'] == 'word':
        return input()
    elif argument['type'] == 'key':
        return key_pressed(argument['allowed'])
    else:
        return argument['type']
        
special_commands = ['stop', 'show controls']

bindings = {
'up'     : ['move', [{'type' : 'move_player'}, {'type' : 'up'}]],
'down'   : ['move', [{'type' : 'move_player'}, {'type' : 'down'}]],
'left'   : ['move', [{'type' : 'move_player'}, {'type' : 'left'}]],
'right'  : ['move', [{'type' : 'move_player'}, {'type' : 'right'}]],
'escape' : ['stop', [{'type' : 'stop'}]],
'/'      : ['show controls', [{'type' : 'show controls'}]],
'v'      : ['magic', [{'type' : 'magic'}, {'type' : 'word', 'descr' : 'Какое магическое оружие ты хочешь использовать'}]],
'z'      : ['attack', [{'type' : 'use_main_weapon' }, {'type' : 'key', 'allowed' : ['up', 'left', 'right', 'down'], 'descr' : 'В какую сторону ты хочешь атаковать?'}]],
'x'      : ['attack', [{'type' : 'use_second_weapon'}, {'type' : 'key', 'allowed' : ['up', 'left', 'right', 'down'], 'descr' : 'В какую сторону ты хочешь атаковать?'}]],
'space'  : ['nothing', [{'type' : 'nothing'}]],
'i'      : ['open inventory', [{'type' : 'open_inventory'}]],
'c'      : ['use', [{'type' : 'use'}, {'type' : 'word', 'descr' : 'Что хотите использовать'}]],
'o'      : ['info', [{'type' : 'info'}]],
'q'      : ['showshopitems', [{'type' : 'showshopitems'}]],
'w'      : ['trade', [{'type' : 'trade'}, {'type' : 'word', 'descr' : 'Что покупаем?'}]],
'e'      : ['remove', [{'type' : 'remove'}, {'type' : 'word', 'descr' : 'Что вы хотите выкинуть?'}]],
'a'      : ['equip', [{'type' : 'equip'}, {'type' : 'word', 'descr' : 'Что вы хотите надеть?'}]],
's'      : ['unequip', [{'type' : 'unequip'}, {'type' : 'word', 'descr' : 'Что вы хотите снять?'}]],
'd'      : ['share', [{'type' : 'share'}, {'type' : 'word', 'descr' : 'Какому игроку вы хотите что-то отдать?'}, {'type' : 'word', 'descr' : 'Что ты бы хотел передать?'}]]
}

russian_bindings = {"." : bindings["/"], "м" : bindings["v"], "я" : bindings["z"], "ч" : bindings["x"], "щ" : bindings["o"],
                    "с": bindings["c"], "ш" : bindings["i"], "й" : bindings["q"], "ц" : bindings["w"], "у" : bindings["e"],
                    "ф": bindings["a"], "ы" : bindings["s"], "в" : bindings["d"], }

bindings.update(russian_bindings)


def input_command(allowed_commands):
    pressed = key_pressed([k for k, c in bindings.items() if c[0] in allowed_commands + special_commands])
    return [get_argument(argument) for argument in bindings[pressed][1]]