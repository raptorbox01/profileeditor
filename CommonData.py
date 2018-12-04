import json
import IniToJson
import sys
import CommonChecker

defaults = {'Blade': {'BandNumber': 3, 'PixPerBand': 144},
            'Blade2': {'BandNumber': 1, 'PixPerBand': 12},
            'Volume': {'Common': 100, 'CoarseLow': 50, 'CoarseMid': 93, 'CoarseHigh': 100},
            'PowerOffTimeout': 300,
            'DeadTime': {'AfterPowerOn': 500, 'AfterBlaster': 500, 'AfterClash': 500},
            'ClashFlashDuration': 72,
            'Motion':
                {'Swing': {'HighW': 6, 'WPercent': 50, 'Circle': 640, 'CircleW': 15},
                 'Spin': {'Enabled': 1, 'Counter': 4, 'W': 70, 'Circle': 640, 'WLow': 40},
                 'Clash': {'HighA': 3500, 'Length': 15, 'HitLevel': -200, 'LowW': 7},
                 'Stab': {'Enabled': 1, 'HighA': 150, 'LowW': 7, 'HitLevel': -200, 'Length': 30, 'Percent': 90},
                 'Screw': {'Enabled': 0, 'LowW': 5, 'HighW': 200}}}

main_sections_default = ['Blade', 'Blade2', 'Volume', 'PowerOffTimeout', 'DeadTime', 'ClashFlashDuration', 'Motion']
main_sections = ['Blade', 'Blade2', 'Volume', 'DeadTime', 'Motion']
blade_keys = ['BandNumber', 'PixPerBand']
volume_keys = ['Common', 'CoarseLow', 'CoarseMid', 'CoarseHigh']
deadtime_keys = ['AfterPowerOn', 'AfterBlaster', 'AfterClash']
motion_keys = ['Swing', 'Spin', 'Clash', 'Stab', 'Screw']
swing_keys = ['HighW', 'WPercent', 'Circle', 'CircleW']
spin_keys = ['Enabled', 'Counter', 'W', 'Circle', 'WLow']
clash_keys = ['HighA', 'Length', 'HitLevel', 'LowW']
stab_keys = ['Enabled', 'HighA', 'LowW', 'HitLevel', 'Length', 'Percent']
screw_keys = ['Enabled', 'LowW', 'HighW']
other_keys = ['PowerOffTimeout', 'ClashFlashDuration']
connection = {'Blade': blade_keys, 'Blade2': blade_keys, 'Volume': volume_keys, 'Deadtime': deadtime_keys, 'Motion': motion_keys}
motion_connection = {'Swing': swing_keys, 'Spin': spin_keys, 'Clash': clash_keys, 'Stab': stab_keys, 'Screw': screw_keys}


class CommonData:

    def __init__(self):
        self.data = {'Blade': {'BandNumber': 3, 'PixPerBand': 144},
            'Blade2': {'BandNumber': 1, 'PixPerBand': 12},
            'Volume': {'Common': 100, 'CoarseLow': 50, 'CoarseMid': 93, 'CoarseHigh': 100},
            'PowerOffTimeout': 300,
            'DeadTime': {'AfterPowerOn': 500, 'AfterBlaster': 500, 'AfterClash': 500},
            'ClashFlashDuration': 72,
            'Motion':
                {'Swing': {'HighW': 6, 'WPercent': 50, 'Circle': 640, 'CircleW': 15},
                 'Spin': {'Enabled': 1, 'Counter': 4, 'W': 70, 'Circle': 640, 'WLow': 40},
                 'Clash': {'HighA': 3500, 'Length': 15, 'HitLevel': -200, 'LowW': 7},
                 'Stab': {'Enabled': 1, 'HighA': 150, 'LowW': 7, 'HitLevel': -200, 'Length': 30, 'Percent': 90},
                 'Screw': {'Enabled': 0, 'LowW': 5, 'HighW': 200}}}

    def update_value(self, key_list: [str], value):
        """
        saves value to data dict to key found by path of keys
        :param key_list: path of keys
        :param value: value to set
        :return:
        """
        data = self.data
        for key in key_list[:-1]:
            data = data[key]
        data[key_list[-1]] = value
        print(data)

    def save_to_file(self, filename):
        text = json.dumps(self.data)
        text = text.replace(r'"', "")
        text = text[1:-1]
        f = open(filename, "w")
        f.write(text)

    def get_default_value(self, key_list: [str])->object:
        """

        :param key_list:
        :param value:
        :return:
        """
        temp_data = defaults
        for key in key_list:
            temp_data = temp_data[key]
        return temp_data

    def load_data_from_text(self, text: str):
        new_data, error = IniToJson.get_json(text)
        if error:
            return None, error, ""
        warning = ""
        Checker = CommonChecker.CommonChecker()
        try:
            #check common keys
            warning, wrong_keys = Checker.common_check_keys(new_data)
            for key in wrong_keys:
                new_data.pop(key)

            #check blade section
            e, w, wrong_data_keys, wrong_keys = Checker.check_blade(new_data, 'blade')
            blade = Checker.get_key(new_data, "Blade")
            if e:
                new_data[blade] = defaults['Blade']
                warning = warning + 'Blade: ' + e + " default values are used;\n"
            if w:
                warning = warning + 'Blade:' + w + "Default values are used;\n"
            for key in wrong_data_keys:
                real_key = Checker.get_key(new_data[blade], key)
                real_def_key = Checker.get_key(defaults['Blade'], key)
                new_data[blade][real_key] = defaults['Blade'][real_def_key]
            for key in wrong_keys:
                new_data.pop(key)

            #check blade2 section
            e, w, wrong_data_keys, wrong_keys = Checker.check_blade(new_data, 'blade2')
            blade2 = Checker.get_key(new_data, 'Blade2')
            for key in wrong_data_keys:
                real_key = Checker.get_key(new_data[blade], key)
                real_def_key = Checker.get_key(defaults['Blade2'], key)
                new_data[blade2][real_key] = defaults['Blade2'][real_def_key]
            for key in wrong_keys:
                new_data.pop(key)
            warning = warning + 'Blade2:' + w + "Default values are used;\n"

            e, w, wrong_data_keys, wrong_keys = Checker.check_volume(new_data)
            if e:
                new_data['Volume'] = defaults['Volume']
                warning = warning + "Volume: " + e + "Default values are used"
            for key in wrong_data_keys:
                volume = Checker.get_key(new_data, "Volume")
                real_key = Checker.get_key(new_data[volume], key)
                real_def_key = Checker.get_key(defaults['Volume'], key)
                new_data[volume][real_key] = defaults['Volume'][real_def_key]
            for key in wrong_keys:
                new_data[volume].pop(key)
            if w:
                warning = warning + 'Volume' + w + "Default values are used;\n"

            for key in main_sections_default:
                real_key = Checker.get_key(new_data, key)
                if not real_key:
                    new_data[key] = defaults[key]
            for key in connection.keys():
                real_top_key = Checker.get_key(new_data, key)
                for secondlevel_key in connection[key]:
                    real_key = Checker.get_key(new_data[real_top_key], secondlevel_key)
                    if not real_key:
                        new_data[real_top_key][secondlevel_key] = defaults[key][secondlevel_key]
            motion_key = Checker.get_key(new_data, 'Motion')
            for key in motion_connection.keys():
                real_top_key = Checker.get_key(new_data[motion_key], key)
                for secondlevel_key in motion_connection[key]:
                    real_key = Checker.get_key(new_data[motion_key][real_top_key], secondlevel_key)
                    if not real_key:
                        new_data[motion_key][real_top_key][real_key] = defaults['Motion'][key][secondlevel_key]






            return new_data, "", warning



        except Exception:
            e = sys.exc_info()[1]
            return None, e.args[0], ""