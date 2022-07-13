from abc import ABC, abstractmethod


class Place(ABC):
    def __init__(self):
        self.name = self.__class__.__name__

    @abstractmethod
    def get_antagonist(self, place):
        pass


class Kostroma(Place):
    def get_antagonist(self):
        print('Orcs hid in the forest')


class Tokyo(Place):
    def get_antagonist(self):
        print('Godzilla stands near a skyscraper')
