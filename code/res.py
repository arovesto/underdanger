walkable_for_players = ['floor', 'exit', 'grass', 'water', 'door', 'slab']

walkable_for_monsters = ['floor', 'exit', 'grass', 'slab']

not_flyable = ['wall', 'brick', 'door']

opaque = ['wall', 'brick'] 

npc = ['лучник','мечник', 'торговец', 'странник']

bad_mobs = ['лучник','мечник']

traders = ['торговец', 'странник']

moving = ['игрок', 'торговец', 'странник', 'лучник', 'мечник']

classes = ['рыцарь', 'волшебник', 'лучник']

proper_magicians = ['волшебник']

proper_stealth = ['лучник']

proper_warrior = ["рыцарь"]

names = [
"Ира", "Максим", "Андрей", "Галя", "Вика", "Маша", "Коля", "Вася", "Саша", "Леша", "Артём", "Аня",
]

positive = ["Да", "Yes", "да", "д", "y", "yes", ""]

list_of_under_mobs_objects = ['floor'] * 10 + ['grass'] * 2

list_of_lands = ['wall'] * 40 + ['water'] * 14 + ['grass'] * 15

list_of_mobs = ['warrior'] * 40 + ['archer'] * 12 + ['merchant'] * 4 + ['magician'] * 1

max_armor_value = 22

bioms_choice = ['lake'] * 2 + ['cave'] * 5 + ['walls'] * 10 + ['ruins']

bioms = {
'lake' : (50, ['water'] * 40 + ['grass']),
'cave' : (15, ['floor'] * 5 + ['wall']),
'walls': (20, ['wall'] * 10 + ['floor']),
'ruins': (10, ['slab'] * 10 + ['fence'] * 3 + ['brick'] * 2),
}

information = {
    'floor' : (1,   '  '),
    'slab'  : (1,   ',,'),
    'grass' : (2,   '&&'),
    'wall'  : (100, '▓▓'),
    'exit'  : (1,   '░░'),
    'unkn'  : (100, '??'),
    'water' : (2,   '~~'),
    'fence' : (100, '╬╬'),
    'door'  : (1,   '╟┤'),
    'brick' : (100, '██'),
}

start_words = '''
Привет, путник! 
Вижу, ты попал сюда, в Подземелье Опасностей. Кажется, тебе надо пояснить, что
здесь происходит. Ты уже понял, что попал в подземелье, но не пугайся. В начале
игры ты появишься в защищенном доме, где ты можешь перевести дух. Но я знаю, что
ты не из тех, кто будет стоять на месте. Тебе надо покинуть свою уютную комнату, и
отправиться на поиски Выхода из подземелья, ведь ты не хочшеь застрять здесь навсегда.
Но не думай, что все так просто. На пути тебе будут мешать различные противники, такие
как мечники (!W) которые постараются ударить тебя своим мечом, или лучники (!A), которые
постараются попасть в тебя из своего лука. Но не бойся, в этом подземелье есть не только
враги. Если тебе повезет, то ты встретишь торговца ($M). У него ты можешь обменять монеты,
на ценные вещи и медикаменты. Какие монеты? А лучники и мечники имеют при себе некие запасы
вещей, которые возможно тебе пригодятся. Кажется, я забыл тебе объяснить как сражаться. Это
Очень просто. У тебя может быть одно оружие в левой руке, и одно в правой. Или одно оружие,
но двуручное. Нажми 'z' чтоб использовать оружие в правой руке и 'х' для оружия в левой руке. Ещё
тебе поможет кнопка '?' на клавиатуре, там тебе покажут все кнопки, которые можно нажимать в
игре. Их довольно много, но не пугайся. Я уверен, ты быстро со всем разберешься. Да, кстати,
в игре все ходят по очереди. У тебя есть какое-то количество очков AP, которые ты тратишь на свои
действия, когда они кончаются, ход переходит к врагам, у которых так же есть эти очки. Еще у тебя
есть твой показатель здоровья HP, если он упадет до нуля, то игра закончится! Однако, у тебя всегда
есть зелья лечения, чтобы справиться с этой проблемой. Так же за убийство противников ты будешь получать 
опыт EXP, который постепенно будет превращаться для тебя в увеличение твоего уровня и твоей силы.

Удачи! Если все готово, то нажми Enter...
'''

classes_info = '''
Теперь коротко о классах. Их в игре есть три, волшебник рыцарь и лучник. Если ты играешь за волшебника,
то у тебя будет немного вещей, которые тебя защищают, однако, у тебя будет хорошая книга с чарами,
которая позволит тебе легко расправляться с самыми разными противниками. Рыцарь же обладает хорошей
защитой а так же хорошим мечом, но это и все. Лучник имеет возможность бить издалека, ну и в целом, как
заядлый охотник, он умеет скрываться куда лучше тех двоих. Выбирай!
'''
                                    
controls = '''
Используй стрелочки на клавиатуре чтобы ходить.
Если нажать 'z' и стрелочку, то ты используешь свое основное оружие
Если нажать 'x' и стрелочку, то ты используешь запасное оружие
Используй 'пробел', чтобы пропустить одно очко действия, и кнопка
Кнопка 'v' чтобы произнести заклинание, и по кнопке 'o' можно узнать,
какие заклинания ты вообще знаешь.

Открыть инвентарь на 'i', используй 'a' чтобы надеть какой-либо предмет, и
'e' чтобы выбросить что-либо. Через 'd' игроки могут обмениваться между
собой предметами. Используй 'c' чтобы использовать что-то из своего инвентаря.
Используй 's' чтобы снять что-то из своего инвентаря.
Во всех этих коммандах следует написать, что ты хочешь использовать после нажатия.

Кнопка 'q' позволяет спросить ближайшего торговца о его товарах, и кнопка 'w' позволяет
купить предмет, если ввести его название.

Чтобы выйти из игры наждми 'ESC'
'''

small_controls = """
игра: z/x - основное/запасное оружие, стрелочки - ходить. ESC выйти.
интвентарь: i/a/s/e/d/c открыть/надеть/снять/выбросить/отдать/использовать
торговля: q/w спросить торговца / приобрести товар.
"""

win_words = """
Ты победил! Ты смог покинуть это подземелье. На этом игра заканчивается. Похоже,
что дальше ты уже сам по себе. Ты всегда можешь сыграть ещё, если хочешь.
"""