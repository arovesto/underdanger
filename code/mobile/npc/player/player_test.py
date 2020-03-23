from code.mobile.npc.player.player import Player
from world.world import World
from code.mobile.npc.mobs.merchant import Merchant
from code.equipment.items import glasses
from code.equipment.weapons import player_knife


def test_init():
    p = Player("Vasyan")
    assert p.name == "Vasyan"


def test_heal():
    p = Player("Vas")
    p.max_hp = 20
    p.hp = 18
    p.heal()
    assert p.hp == 20


def test_do_showshopitems():
    w = World()
    p = w.add(Player('Petya'), (0, 0))
    p.showshopitems()
    assert p.last_happend == 'Petya спросил никого о торгах'

    m = w.add(Merchant(), (0, 10)).start_equip()
    p.showshopitems()
    assert p.last_happend == 'Petya спросил никого о торгах'

    w.add(Merchant(), (0, 1)).start_equip()
    p.showshopitems()
    assert p.last_happend != 'Petya спросил никого о торгах'


def test_do_share():
    p1 = Player('Штирлиц')
    p1_inv_before = p1.inventory
    p1.position = (10, 0)
    p2 = Player('Исаев')
    p2_inv_before = p2.inventory
    p2.position = (0, 0)
    w = World()
    w.players[(0, 0)] = p2
    p1.world = w
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


def test_do_equip():
    p = Player('Petya')
    p.inventory = [player_knife()]
    assert p.equipment['mainhand'] is None
    p.equip('меч')
    assert p.equipment['mainhand'].name == 'меч'
    assert p.equipment['mainhand'].user == p
