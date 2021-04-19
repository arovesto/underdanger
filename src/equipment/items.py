from src.geometry.geometry import sub, manhattan
from src.geometry.direction import where_to_go
from src.equipment.magic import small_ring, blindness, sleeppy
from data.res import proper_magicians, proper_warrior
from src.equipment.armor import heavy_armor
from src.util.words import name_to_genitive


class Item:
    tag = "usable"

    def __init__(self, name, look):
        self.name = name
        self.look = look
        self.kind = 'usable'
        self.price = 0
        self.description = ""

    def __eq__(self, other):
        return other.name == self.name

    def __hash__(self):
        return hash(self.name)

    def use(self, user):
        self.remove(user)
        user.exp += 1
        return "{} выглядит очень мудро в очках и получает опыт".format(user.name)

    def __str__(self):
        if self.price == 0:
            return self.name + ' - ' + self.description
        return '{} за {}'.format(self.name + ' - ' + self.description, self.price)

    def remove(self, user):
        user.inventory.remove(self)

    def info(self):
        return dict(
            name=self.name,
            look=self.look,
            kind=self.kind,
            price=self.price,
            description=self.description,
        )


class HealingPotion(Item):
    def __init__(self, healing_hp, name):
        super().__init__(name, '()')
        self.healing_hp = healing_hp
        self.description = "восстанавливает здоровье на {}".format(healing_hp)

    def use(self, user):
        self.remove(user)
        if user.hp + self.healing_hp < user.max_hp:
            user.hp += self.healing_hp
            return '{} был излечен на {}'.format(user.name, self.healing_hp)
        else:
            user.hp = user.max_hp
            return '{} здоровье было максимизировано'.format(user.name)


class SpeedPotion(Item):
    def __init__(self, ap_increase, name):
        super().__init__(name, '<>')
        self.ap_increase = ap_increase
        self.description = "увеличивает максимальный AP на {}".format(self.ap_increase)

    def use(self, user):
        self.remove(user)
        user.max_ap += self.ap_increase
        return '{} максимальное AP было увеличено на {}'.format(user.name, self.ap_increase)


class APRestorePotion(Item):
    def __init__(self):
        super().__init__('зелье отдыха', '**')
        self.description = "восстанавливает АP"

    def use(self, user):
        self.remove(user)
        user.ap = user.max_ap
        return 'AP {} были восстановлены'.format(name_to_genitive(user.name))


class HealthSpeedPotion(Item):
    def __init__(self, health_increase, name):
        super().__init__(name, "++")
        self.health_increase = health_increase
        self.description = "увеличивает максимальный НP на {}".format(self.health_increase)

    def use(self, user):
        self.remove(user)
        user.max_hp += self.health_increase
        return "{} максимальное HP было увеличено на {}".format(user.name, self.health_increase)


class Map(Item):
    def __init__(self, name):
        super().__init__(name, "[]")
        self.description = "показывает, где выход"

    def use(self, user):
        closest_exit = user.world.nearest_exit_to(user.position)
        delta_to_exit = sub(closest_exit, user.position)
        return "Посмотрев на карту {} увидел, что ему надо идти на {}, ещё {} шагов" \
            .format(user.name, where_to_go(delta_to_exit), manhattan(closest_exit, user.position))


class Undying(Item):
    def __init__(self, name):
        super().__init__(name, "xx")
        self.description = "если ситуация критическая, то поможет"

    def use(self, user):
        if user.hp <= 4:
            self.remove(user)
            user.hp = user.max_hp * 2 // 3
            user.ap = user.max_ap
            return "{} обнаружил в себе мощный прилив сил".format(user.name)
        return "{} не умирает, у него пока все хорошо".format(user.name)


class Scroll(Item):
    def __init__(self, name, magic, better_form=None):
        super().__init__(name, "?/")
        self.name = name
        self.magic = magic
        self.better_form = better_form
        assert magic.name == better_form.name
        self.description = 'учит магии "{}"'.format(self.magic.name)

    def use(self, user):
        self.remove(user)
        if user.class_ in proper_magicians and self.better_form:
            user.magicbook.append(self.better_form)
            self.better_form.user = user
            return "{} выучил магию {} очень хорошо".format(user.name, self.magic.name)
        else:
            user.magicbook.append(self.magic)
            self.magic.user = user
            return "{} выучил магию {}".format(user.name, self.magic.name)


class MoneyBag(Item):
    def __init__(self, money):
        super().__init__('мешок монеток', '$$')
        self.money = money
        self.description = "содержит в себе деньги"

    def use(self, user):
        self.remove(user)
        user.money += self.money
        return 'В мешке было {} денег'.format(self.money)


class Bag(Item):
    def __init__(self, *items, name='мешок'):
        super().__init__(name, '%%')
        self.items = items
        self.description = "содержит в себе предметы"

    def use(self, user):
        self.remove(user)
        for item in self.items:
            user.inventory.append(item)
        return '{} открыл мешок с: {}'.format(user.name, ', '.join(item.name for item in self.items))


# TODO boost existing magic. Scrolls should be more powerfull for Wizard
class MagicBoost(Item):
    def __init__(self, magic, name='усиление'):
        super().__init__(name, '%%')
        self.magic = magic
        self.description = "усиливает магию {}".format(magic.name)

    def use(self, user):
        if self.magic in user.magicbook:
            self.remove(user)
            user.magicbook.remove(self.magic)
            user.magicbook.append(self.magic)
            self.magic.user = user
            return "{} усилил свою магию".format(user.name)
        return "{} не имеет магии {}".format(user.name, self.magic.name)


class WarriorTankArmor(Item):
    def __init__(self, armor, name="броня"):
        super().__init__(name, "%%")
        self.armor = armor
        self.description = "Только для рыцарей! Тяжелое обмундрование, которое не всякий сможет даже распаковать"

    def use(self, user):
        if user.class_ in proper_warrior:
            self.remove(user)
            armor = heavy_armor()
            armor.equip(user)
            return "{} надел тяжелую экипировку".format(user.name)
        return "{} слишком слаб для тяжелой экипировки".format(user.name)


def glasses(): return Item('очки', 'oo')


def new_map(): return Map("карта")


def undying(): return Undying("последнее средство")


def heal_boost_potion(): return HealthSpeedPotion(3, "живучесть")


def small_heal_potion(): return HealingPotion(6, 'малое восстановление')


def normal_heal_potion(): return HealingPotion(12, 'обычное восстановление')


def big_heal_potion(): return HealingPotion(18, 'большое восстановление')


def money_bag(): return MoneyBag


def bag(): return Bag


def standard_speed_potion(): return SpeedPotion(1, name='ускорение')


def big_speed_potion(): return SpeedPotion(2, name='большое ускорение')


def scroll_of_blindness(): return Scroll("свиток ослепления", blindness(), blindness(2, 1))


def scroll_of_ring(): return Scroll("свиток кольца", small_ring(), small_ring(7))


def scroll_of_sleeppy(): return Scroll("свиток усыпления", sleeppy(), sleeppy(0.3, 20))


def rest_potion(): return APRestorePotion()


def super_armor(): return WarriorTankArmor(armor=10, name="тяжелый доспех")
