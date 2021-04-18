from src.equipment.equipment import Equipment
from data.res import proper_magicians, proper_stealth


class Armor(Equipment):
    kind = 'armor'
    look = '!!'

    def __init__(self, block_value, bodyparts, name, use_parts=None, description=None):
        self.bodyparts = bodyparts
        if description:
            self.description = description
        else:
            self.description = "Дает {} защиты".format(block_value)
        self.block = block_value
        self.name = name

    def info(self):
        inf = super(Armor, self).info()
        inf["block_value"] = self.block
        return inf


class MagicArmor(Armor):
    kind = 'armor'
    look = '!!'

    def equip(self, user):
        self.user = user
        if user.class_ in proper_magicians:
            self.block *= 2
            self.user.max_hp += 2
            self.user.see += 1
        for part in self.bodyparts:
            self.user.equipment[part] = self
        return self


class StealthCloak(Armor):
    kind = 'armor'
    look = '!!'

    def equip(self, user):
        self.user = user
        if user.class_ in proper_stealth:
            self.user.obscurity *= 1.5
            self.block += 3
        else:
            self.user.obscrurity *= 1.2
        for part in self.bodyparts:
            self.user.equipment[part] = self
        return self

    def unequip(self):
        if self.user.class_ in proper_stealth:
            self.user.obscurity /= 1.5
        else:
            self.user.obscrurity /= 1.2
        for part in self.bodyparts:
            self.user.equipment[part] = None
        self.user.inventory.append(self)


# TODO add legend armor for warrior ONLY (hard shit)

def helmet(): return Armor(2, ['голова'], 'шлем')


def rogue_helmet(): return Armor(3, ['голова'], 'хороший шлем')


def round_shield(): return Armor(6, ['дополнительное'], 'круглый щит')


def pants(): return Armor(1, ['ноги'], 'штаны')


def tunic(): return Armor(1, ['тело'], 'туника')


def chain_mail(): return Armor(4, ['тело'], 'кольчуга')


def metal_mail(): return Armor(6, ['тело'], 'броня')


def shoes(): return Armor(1, ['обувь'], 'сапоги')


def aluminium_mail(): return Armor(8, ['тело'], 'алюминиевая кольчуга')


def heavy_armor(): return Armor(12, ['тело'], "тяжелейшая броня")


def magic_tunic(): return MagicArmor(4, ["trunk"], "волшебная туника", description="Волшебнику это понравится")


def stealth_cloak(): return StealthCloak(4, ['тело'], "плащ невидимости",
                                         description="Добавляет владельцу маскировки. Отлично подойдет лучнику")
