from abc import abstractmethod

from heroes import SuperHero
from places import Place


class InfoChannel:
    name = ''

    @abstractmethod
    def get_message(self):
        pass


class TV(InfoChannel):
    name = 'TV'

    @staticmethod
    def get_message():
        message = 'An emergency broadcast on channel 7:'
        return message


class NewsPaper(InfoChannel):
    name = 'NewsPaper'

    @staticmethod
    def get_message():
        message = 'Only in our hot off the press paper:'
        return message


class MassMedia:
    _channels_choices = {
        'All': (TV, NewsPaper),
        'TV': (TV,),
        'NewsPaper': (NewsPaper,),
    }
    channels_choices_keys = _channels_choices.keys()

    def create_news(self, hero: SuperHero, place: Place, channel: str = 'TV'):
        '''
        Create news for info channel, chosen in channel variable.
        Choices are: 'All', 'TV', 'NewsPaper'
        '''
        choice = self._channels_choices.get(channel, )
        if choice:
            for channel in self._channels_choices[channel]:
                message = channel.get_message()
                print(f'{message} {hero} saved the {place}!')
