from typing import Union

from heroes import Superman, ChackNorris, SuperHero
from mass_media import MassMedia
from places import Kostroma, Tokyo, Earth


def save_the_place(hero: SuperHero, place: Union[Kostroma, Tokyo]):
    hero.find(place)
    hero.attack()
    if hero.can_use_ultimate_attack:
        hero.ultimate()
    mass_media = MassMedia()
    mass_media.create_news(hero, place, 'All')


if __name__ == '__main__':
    save_the_place(Superman(), Kostroma())
    print('-' * 20)
    save_the_place(ChackNorris(), Tokyo())
    print('-' * 20)
    save_the_place(Superman(False), Earth())
