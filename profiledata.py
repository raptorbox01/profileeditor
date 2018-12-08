from typing import Sequence

default_profile = {'AfterWake': {},
                   'PowerOn': {'Blade': {'Speed': 144}},
                   'WorkingMode': {'Color': [0, 99, 18], 'Flaming': 0, 'FlickeringAlways': 1},
                   'PowerOff': {'Blade': {'Speed': 144, 'MoveForward': 0}},
                   'Flaming': {'Size': {'Min': 2, 'Max': 9}, 'Speed': {'Min': 12, 'Max': 27},
                               'Delay_ms': {'Min': 54, 'Max': 180},
                               'Colors': [[180, 0, 0], [144, 144, 0], [153, 90, 0], [153, 45, 0]]},
                   'Flickering': {'Time': {'Min': 90, 'Max': 360}, 'Brightness': {'Min': 50, 'Max': 100}},
                   'Blaster': {'Color': 'random', 'Duration_ms': 720, 'SizePix': 7},
                   'Clash': {'Color': [255, 0, 0], 'Duration_ms': 720, 'SizePix': 11},
                   'Stab': {'Color': [255, 0, 0], 'Duration_ms': 720, 'SizePix': 11},
                   'Lockup': {'Flicker': {'Color': [255, 0, 0], 'Time': {'Min': 45, 'Max': 80},
                                          'Brightness': {'Min': 50, 'Max': 100}},
                              'Flashes': {'Period': {'Min': 15, 'Max': 25}, 'Color': [255, 0, 0], 'Duration_ms': 50,
                                          'SizePix': 7}},
                   'Blade2':
                       {'WorkingMode': {'Color': [231, 231, 231]},
                        'Flaming': {'AlwaysOn': 1, 'Size': {'Min': 2, 'Max': 9}, 'Speed': {'Min': 12, 'Max': 27},
                                    'Delay_ms': {'Min': 54, 'Max': 180},
                                    'Colors': [[180, 0, 0], [144, 144, 0], [153, 90, 0], [153, 45, 0]]},
                        'Flickering': {'AlwaysOn': 1, 'Time': {'Min': 90, 'Max': 360},
                                       'Brightness': {'Min': 50, 'Max': 100}}, 'DelayBeforeOn': 5}}


class Profiles:

    def __init__(self):
        self.data = dict()

    def get_profiles_list(self):
        """
        returns list of profile keys
        :return:
        """
        return self.data.keys()

    def add_profile(self, name: str):
        """
        adds profile with given name and default values
        :param name: name of profile
        :return:
        """
        self.data[name] = {'AfterWake': {},
                           'PowerOn': {'Blade': {'Speed': 144}},
                           'WorkingMode': {'Color': [0, 99, 18], 'Flaming': 0, 'FlickeringAlways': 1},
                           'PowerOff': {'Blade': {'Speed': 144, 'MoveForward': 0}},
                           'Flaming': {'Size': {'Min': 2, 'Max': 9}, 'Speed': {'Min': 12, 'Max': 27},
                                       'Delay_ms': {'Min': 54, 'Max': 180},
                                       'Colors': []},
                           'Flickering': {'Time': {'Min': 90, 'Max': 360}, 'Brightness': {'Min': 50, 'Max': 100}},
                           'Blaster': {'Color': 'random', 'Duration_ms': 720, 'SizePix': 7},
                           'Clash': {'Color': [255, 0, 0], 'Duration_ms': 720, 'SizePix': 11},
                           'Stab': {'Color': [255, 0, 0], 'Duration_ms': 720, 'SizePix': 11},
                           'Lockup': {'Flicker': {'Color': [255, 0, 0], 'Time': {'Min': 45, 'Max': 80},
                                                  'Brightness': {'Min': 50, 'Max': 100}},
                                      'Flashes': {'Period': {'Min': 15, 'Max': 25}, 'Color': [255, 0, 0],
                                                  'Duration_ms': 50,
                                                  'SizePix': 7}}}

    def delete_profile(self, name: str):
        """
        deletes profile by key
        :param name: name of profile
        :return:
        """
        self.data.pop(name)

    def get_default(self, path: Sequence[str]) -> object:
        """
        gets default value for key path
        :param path: pat of keys
        :return: default value
        """
        data = default_profile
        for key in path:
            data = data[key]
        return data

    def get_value(self, path: Sequence[str], profile: str) -> object:
        """
        gets value of field configured with pat for profile
        :param path: path of keys
        :param profile: profile key
        :return: value
        """
        data = self.data[profile]
        for key in path:
            data = data[key]
        return data
