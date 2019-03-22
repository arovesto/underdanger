from weapons import  player_bow, player_knife, metal_bow, player_small_knife, whip, spear
from magic import small_ring, magic_bomb, blindness, sleeppy
from player import Player
from armor import helmet, pants, chain_mail, tunic, round_shield, stealth_cloak
from items import rest_potion, normal_heal_potion, scroll_of_sleeppy, super_armor


# TODO Check Spear and Cloak on working + magic of sleepy (test new mechanics)

def generate_player(class_, name):
    if class_ == 'рыцарь':
        return MediumFighter(name).start_equip()
    elif class_ == 'волшебник':
        return Wizard(name).start_equip()
    elif class_ == 'лучник':
        return Scout(name).start_equip()
    raise ValueError("Плохое имя класса добралось куда не надо")

class MediumFighter(Player):   
    def __init__(self, name):
        super().__init__(name)
        self.max_hp = 35
        self.max_ap = 4
        self.obscurity = 1.1
        self.hp, self.ap = self.max_hp, self.max_ap
        self.descr = 'Обычный рыцарь, имеет щит и меч.'
        self.class_ = 'рыцарь'
        
    def start_equip(self):      
        self.inventory += [normal_heal_potion(), rest_potion(), metal_bow()]
        round_shield().equip(self)
        player_knife().equip(self)
        helmet().equip(self)
        chain_mail().equip(self)
        pants().equip(self)
        return self
    
class Wizard(Player):
    def __init__(self, name):
        super().__init__(name)
        self.max_hp = 28
        self.max_ap = 5
        self.obscurity = 1.3
        self.hp, self.ap = self.max_hp, self.max_ap
        self.class_ = 'волшебник'
        self.descr = 'Хитрый маг, однако слабоват в обычном бою.'

    def start_equip(self):      
        self.inventory += [normal_heal_potion(), rest_potion(), player_small_knife(), scroll_of_sleeppy()]
        self.magicbook += [small_ring().equip(self), magic_bomb().equip(self)]
        tunic().equip(self)
        return self
         
class Scout(Player):
    def __init__(self, name):
        super().__init__(name)
        self.max_hp = 24
        self.max_ap = 6
        self.obscurity = 2.0
        self.hp, self.ap = self.max_hp, self.max_ap
        self.class_ = 'лучник'
        self.descr = 'Ловкий охотник с хорошим оружием'

    def start_equip(self):
        tunic().equip(self)
        pants().equip(self)
        player_bow().equip(self)
        self.inventory += [whip(), rest_potion(), rest_potion(), rest_potion(), normal_heal_potion(), player_small_knife()]
        return self

    