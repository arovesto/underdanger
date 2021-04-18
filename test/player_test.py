from src.mobile.npc.player.player import Player
from src.mobile.npc.mobs.merchant import Merchant
from src.equipment.items import glasses
from src.equipment.weapons import player_knife


def test_init(player):
    assert player.name == "Vasiliy"


def test_heal(player):
    player.max_hp = 20
    player.hp = 18
    player.heal()
    assert player.hp == 20


def test_do_showshopitems(world):
    player = world.add(Player('Petya'), (0, 0))
    player.showshopitems()
    assert player.last_happend == 'Petya спросил никого о торгах'

    m = world.add(Merchant(), (0, 10)).start_equip()
    player.showshopitems()
    assert player.last_happend == 'Petya спросил никого о торгах'

    world.add(Merchant(), (0, 1)).start_equip()
    player.showshopitems()
    assert player.last_happend != 'Petya спросил никого о торгах'


def test_do_share(world):
    p1 = Player('Штирлиц')
    p1_inv_before = p1.inventory
    p1.position = (10, 0)
    p2 = Player('Исаев')
    p2_inv_before = p2.inventory
    p2.position = (0, 0)
    world.players[(0, 0)] = p2
    p1.world = world
    p1.inventory += [glasses()]
    p1.share('Исаев', 'очки')
    assert p1.last_happend == 'Штирлиц слишком далеко от Исаев'
    assert p2.inventory == p2_inv_before

    p1.position = (0, 0)
    p1.share('Исаев', 'очки')
    assert p1.last_happend == 'Штирлиц передал очки в руки Исаев'
    assert p2.inventory[-1].name == 'очки'
    assert len(p1.inventory) == len(p1_inv_before)

    p1.share('Исаев', 'очки')
    assert p1.last_happend == "Штирлиц не может дать очки в руки Исаев"


def test_do_equip(player):
    player.inventory = [player_knife()]
    assert player.equipment['основное'] is None
    player.equip('меч')
    assert player.equipment['основное'].name == 'меч'
    assert player.equipment['основное'].user == player
