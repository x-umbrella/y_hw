from abc import ABC, abstractmethod
from attacks import GunFire, Laser


class SuperHero(ABC):

    def __init__(self, name, can_use_ultimate_attack=True):
        self.name = name
        self.can_use_ultimate_attack = can_use_ultimate_attack

    def find(self, place):
        place.get_antagonist()

    @abstractmethod
    def attack(self):
        pass

    def ultimate(self):
        pass


class ChackNorris(SuperHero, GunFire):
    def __init__(self, name, can_use_ultimate_attack=True):
        super().__init__(name, can_use_ultimate_attack)
    
    def attack(self):
        self.fire_a_gun()


class Superman(SuperHero, Laser):
    def __init__(self, name, can_use_ultimate_attack=True):
        super().__init__(name, can_use_ultimate_attack)

    def attack(self):
        print('Kick')

    def ultimate(self):
        self.incinerate_with_lasers()