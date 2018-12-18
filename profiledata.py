from typing import Sequence, Tuple
import json
import IniToJson
import profilechecker

default_profile = {'AfterWake': {},
                   'PowerOn': {'Blade': {'Speed': 144}},
                   'WorkingMode': {'Color': [0, 255, 0], 'Flaming': 0, 'FlickeringAlways': 1},
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
                              'Flashes': {'Period': {'Min': 15, 'Max': 25}, 'Color': [255, 0, 0], 'Duration_ms': 50,
                                          'SizePix': 7}},
                   'Blade2': {
                       'IndicateBlasterClashLockup': 1, 'DelayBeforeOn': 200,
                       'WorkingMode': {'Color': [0, 255, 0]},
                        'Flaming': {'AlwaysOn': 1, 'Size': {'Min': 2, 'Max': 9}, 'Speed': {'Min': 12, 'Max': 27},
                                    'Delay_ms': {'Min': 54, 'Max': 180},
                                    'Colors': []},
                        'Flickering': {'AlwaysOn': 1, 'Time': {'Min': 90, 'Max': 360},
                                       'Brightness': {'Min': 50, 'Max': 100}}}}

aux_key = 'AuxLeds'


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
                           'WorkingMode': {'Color': [0, 0, 255], 'Flaming': 0, 'FlickeringAlways': 1},
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
                                                  'SizePix': 7}},
                           'Blade2':{
                               'IndicateBlasterClashLockup': 1, 'DelayBeforeOn': 200,
                               'WorkingMode': {'Color': [0, 0, 255]},
                                'Flaming': {'AlwaysOn': 1, 'Size': {'Min': 2, 'Max': 9},
                                            'Speed': {'Min': 12, 'Max': 27},
                                            'Delay_ms': {'Min': 54, 'Max': 180},
                                            'Colors': []},
                                'Flickering': {'AlwaysOn': 1, 'Time': {'Min': 90, 'Max': 360},
                                               'Brightness': {'Min': 50, 'Max': 100}}}
        }

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

    def update_value(self, path: Sequence[str], profile: str, value: object):
        """
        updates field for given keys in given profile, makes in given value
        :param path: key path
        :param profile: profile
        :param value: given new value
        :return:
        """
        try:
           data = self.data[profile]
           for key in path[:-1]:
                data = data[key]
           data[path[-1]] = value
        except (KeyError, IndexError):
            print("no such key or keypath is empty") # to do logging
        print(data)

    def save_color(self, path: Sequence[str], color: Sequence[int], profile: str):
        """
        saves color given as a list of rgb components to path in profiledata dict
        :param path: path of keys
        :param color: rgb components
        :param profile: current profile
        :return:
        """
        try:
            data = self.data[profile]
            for key in path[:-1]:
                data = data[key]
            data[path[-1]].append(color)
        except (IndexError, TypeError, ValueError):
            print ("wrong keypath or color data") # to do logging
        print(data)

    def get_colors(self, path: Sequence[str], profile: str)->Sequence[str]:
        """
        gets colors list for profile and path
        :param path: list of keys
        :param profile: current profile
        :return: list of colors
        """
        try:
            data = self.data[profile]
            for key in path:
                data = data[key]
            return data
        except (KeyError):
            print("Wrong keys used") #to do logging
            return None

    def delete_color(self, path: Sequence[int], color: Sequence[int], profile: str):
        """
        deletes color given as a list of rgb components from path in profiledata dict
        :param path: path of keys
        :param color: rgb components
        :param profile: current profile
        :return:
        """
        try:
            data = self.data[profile]
            for key in path[:-1]:
                data = data[key]
            data[path[-1]].remove(color)
        except (IndexError, TypeError, ValueError):
            print("wrong keypath or color data")  # to do logging
        print(data)

    def save_aux(self, aux: str, effect: str, profile: str):
        """
        save aux effect to effect in profile
        :param aux:
        :param effect:
        :param profile:
        :return:
        """
        data = self.data[profile][effect]
        if aux_key not in data.keys():
            data[aux_key] = [aux]
        else:
            data[aux_key].append(aux)
        print(data)

    def delete_aux(self, aux: str, effect: str, profile: str):
        try:
            data = self.data[profile][effect]
            data[aux_key].remove(aux)
            if data[aux_key] == []:
                data.pop(aux_key)
        except (IndexError, KeyError):
            print("Incorrects key or aux name") # to do logging
        print(data)

    def get_aux_effects(self, effect: str, profile: str):
        """
        gets list of auxeffects for selected profile and effect
        :param effect: effect to get aux effects for
        :param profile: profile get auxeffects for
        :return:
        """
        data = self.data
        data = data[profile][effect]
        return data.get(aux_key, [])


    def save_to_file(self, filename:str):
        """
        saves to filename as pseudo-json (no quotes)
        :param filename: name of file to save
        :return:
        """
        text = json.dumps(self.data)
        text = text.replace(r'"', "")
        text = text[1:-1]
        f = open(filename, "w")
        f.write(text)

    def get_default_value(self, key_list: [str]) -> object:
        """
        get value from defaults using key path
        :param key_list: path of keys
        :return: value
        """
        temp_data = default_profile
        for key in key_list:
            temp_data = temp_data[key]
        return temp_data

    def check_section(self, new_data: dict, check_function: callable, param: str, required: bool, default: dict)\
            -> Tuple[str, dict]:
        """
        checks section of loaded from text data
        :param new_data: data
        :param check_function: function to check with
        :param param: key of section
        :param required: is this section required
        :param default: needed part of default dict
        :return: warning text, new_data correcter
        """
        checker = profilechecker.ProfileChecker()
        warning = ""
        e, w, wrong_data_keys, wrong_keys = check_function(new_data, param.lower())
        if required and e:
            new_data[param] = default[param]
            warning = warning + param + ': ' + e + " default values are used;\n"
        section_key = checker.get_key(new_data, param)
        if w:
            warning = warning + param + ': ' + w + "Default values are used;\n"
        for key in wrong_data_keys:
            real_key = checker.get_key(new_data[section_key], key)
            real_def_key = checker.get_key(default[param], key)
            new_data[section_key][real_key] = default[param][real_def_key]
        for key in wrong_keys:
            new_data[section_key].pop(key)
        return warning, new_data

    def get_defaults_for_absent(self, new_data):
        """
        checks if some data is absent and loads default
        :param new_data: dict with data
        :return: data updated with defaults values
        """
        checker = profilechecker.ProfileChecker()
        for key in checker.effects_keys:
            real_key = checker.get_key(new_data, key)
            if not real_key:
                new_data[key] = default_profile[key]
        for key in connection.keys():
            real_top_key = checker.get_key(new_data, key)
            for secondlevel_key in connection[key]:
                real_key = checker.get_key(new_data[real_top_key], secondlevel_key)
                if not real_key:
                    new_data[real_top_key][secondlevel_key] = defaults[key][secondlevel_key]
        motion_key = checker.get_key(new_data, 'Motion')
        for key in motion_connection.keys():
            real_top_key = checker.get_key(new_data[motion_key], key)
            for secondlevel_key in motion_connection[key]:
                real_key = checker.get_key(new_data[motion_key][real_top_key], secondlevel_key)
                if not real_key:
                    new_data[motion_key][real_top_key][secondlevel_key] = defaults['Motion'][key][secondlevel_key]
        return new_data

    def load_data_from_text(self, text: str):
        """
        loads data from texts
        :param text: text with data
        :return:
        """
        new_data, error = IniToJson.get_json(text)
        if error or new_data is None:
            return None, error, ""
        if not isinstance(new_data, dict):
            return None, "Wrong profile data format", ""
        for profile in new_data.keys():
            pass
        return new_data, "", ""

