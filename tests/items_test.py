from src.equipment.items import rest_potion


def test_APRestorePotion(player):
    player.inventory.append(rest_potion())
    player.ap = 3
    player.max_ap = 10
    assert player.ap != player.max_ap
    player.use(rest_potion().name)
    assert player.ap == player.max_ap
