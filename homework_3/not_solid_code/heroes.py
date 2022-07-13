from abc import abstractmethod
from random import randint

from antagonistfinder import AntagonistFinder


class Weapon:
    name = 'Weapon'

    @abstractmethod
    def use_weapon(self):
        pass


class Legs(Weapon):
    name = 'Legs'

    def _roundhouse_kick(self):
        print('Bump')

    def use_weapon(self):
        self._roundhouse_kick()


class Lasers(Weapon):
    def _incinerate_with_lasers(self):
        print('Wzzzuuuup!')

    def use_weapon(self):
        self._incinerate_with_lasers()


class Gun(Weapon):
    def _fire_a_gun(self):
        print('PIU PIU')

    def use_weapon(self):
        self._fire_a_gun()


class SuperHero:

    def __init__(self, name, can_use_ultimate_attack=True):
        self.name = name
        self.can_use_ultimate_attack = can_use_ultimate_attack
        self.finder = AntagonistFinder()
        self.usual_weapons = ()

    def find(self, place):
        self.finder.get_antagonist(place)

    def attack(self):
        if self.usual_weapons:
            weapons_count = len(self.usual_weapons)
            weapon_to_use = randint(0, weapons_count - 1)
            self.usual_weapons[weapon_to_use].use_weapon()

    def ultimate(self):
        pass

    def __str__(self):
        return self.name


class Superman(SuperHero):

    def __init__(self, can_use_ultimate_attack=True):
        super(Superman, self).__init__('Clark Kent', can_use_ultimate_attack)
        self.usual_weapons = (Legs(), Gun())
        self.ultimate_weapon = Lasers()

    def ultimate(self):
        self.ultimate_weapon.use_weapon()


class ChackNorris(SuperHero):

    def __init__(self):
        super(ChackNorris, self).__init__('Chack Norris', False)
        self.usual_weapons = (Legs(), Gun())
