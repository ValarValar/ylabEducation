from abc import abstractmethod


class Place:
    name = ''

    @abstractmethod
    def get_antagonist(self):
        pass


class Kostroma(Place):
    name = 'Kostroma'

    def get_antagonist(self):
        print('Orcs hid in the forest')

    def __str__(self):
        return self.name


class Tokyo(Place):
    name = 'Tokyo'

    def get_antagonist(self):
        print('Godzilla stands near a skyscraper')

    def __str__(self):
        return self.name


class Earth(Place):
    coordinates = [15.3515, 87.3429, 50.4423]

    def get_antagonist(self):
        print('Humans are starting nuclear war')

    def __str__(self):
        return f'planet on coords: {self.coordinates}'
