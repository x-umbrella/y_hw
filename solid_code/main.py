from typing import Union
from places import Kostroma, Tokyo
from heroes import ChackNorris, Superman, SuperHero
from mass_media import MassMedia


def save_the_place(hero: SuperHero, place: Union[Kostroma, Tokyo]):
    hero.find(place)
    hero.attack()
    if hero.can_use_ultimate_attack:
        hero.ultimate()
    MassMedia.create_news_newspaper(hero, place)


if __name__ == '__main__':
    save_the_place(Superman('Clark Kent'), Kostroma())
    print('-' * 20)
    save_the_place(ChackNorris('Chack Norris', False), Tokyo())
