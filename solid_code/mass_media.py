from random import random


class MassMedia:
    planets = [round(random(), 3) for i in range(3)]
    
    @classmethod
    def create_news_newspaper(cls, hero, place):
        print(f'News from newspaper: {hero.name} saved the {place.name}!')
        cls.notify_planets()

    @classmethod
    def notify_planets(cls):
        print(f'planet data has also been notified: {cls.planets}')