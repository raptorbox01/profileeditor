from CommonChecks import *
from typing import *



class CommonChecker:
    common_keys = ['blade', 'blade2', 'volume', 'powerofftimeout', 'deadtime', 'clashflashduration', 'motion']
    common_keys_cap = ['Blade', 'Blade2', 'Volume', 'PowerOffTimeout', 'Deadtime', 'ClashFlashDuration', 'Motion']
    motion_keys = ['swing', 'spin', 'clash', 'stab', 'screw']
    motion_keys_cap = ['Swing', 'Spin', 'Clash', 'Stab', 'Screw']
    blade_keys = ['bandnumber', 'pixperband']
    volume_keys = ['common', 'coarselow', 'coarsemid', 'coarsehigh']
    deadtime_keys = ['afterpoweron', 'afterblaster', 'afterclash']
    swing_keys = ['highw', 'wpercent', 'circle', 'circlew']
    spin_keys = ['enabled', 'counter', 'w', 'circle', 'wlow']
    clash_keys = ['higha', 'length', 'hitlevel', 'loww']
    stab_keys = ['enabled', 'higha', 'loww', 'hitlevel', 'length', 'percent']
    screw_keys = ['enabled', 'loww', 'highw']

    max_band = 8
    max_leds = 144
    max_total_leds = 2000
    big_number = 9999
    w_high = 500
    w_low = 1
    a_high = 99999
    a_low = 100

    def common_check_keys(self, data: dict) -> Tuple[str, Sequence[str]]:
        """

        :param data:
        :param keys:
        :return:
        """
        return check_keys(data, self.common_keys)

    def motion_check_keys(self, data: dict) -> Tuple[str, Sequence[str]]:
        """

        :param data:
        :param keys:
        :return:
        """
        if not isinstance(data, dict):
            return "Wrong motion data format;\n", []
        return check_keys(data, self.motion_keys)

    def get_key(self, data: dict, key: str):
        """

        :param key:
        :param dict:
        :return:
        """
        for new_key in data.keys():
            if key.lower() == new_key.lower():
                return new_key
        return ""

    def check_blade(self, data: dict, key: str) -> (str, str, [str]):
        """
        checks blade paramenters: bandbumber and pixperband
        :param data: dict with values
        :param key: key to check (blade or blade2)
        :return: error and warning messages or empty strings and list of wrong keys
        """
        wrong_data_keys = []
        blade, error = check_existance(data, key)
        if error:
            return error, "", [], []
        warning, wrong_keys = check_keys(blade, self.blade_keys)
        w = check_number(blade, 'bandnumber', 1, self.max_band)
        if w:
            wrong_data_keys.append('bandnumber')
        band = get_value(blade, 'bandnumber')
        warning += w
        w = check_number(blade, 'pixperband', 1, self.max_leds)
        warning += w
        if w:
            wrong_data_keys.append('pixperband')
        leds = get_value(blade, 'pixperband')
        if leds and band and isinstance(leds, int) and isinstance(band, int):
            if leds * band > self.max_total_leds:
                w += "total leds per blade must be less then % i;\n" % self.max_total_leds
                wrong_data_keys.append('bandnumber')
                wrong_data_keys.append('pixperband')
        return "", warning, wrong_data_keys, wrong_keys


    def check_volume(self, data: dict, param: str) -> (str, str, [str], [str]):
        """
        checks if folume parameter is correct
        :param data: dict with wolume settings
        :return: error message or ""
        """
        wrong_data_keys = []
        volume = get_real_key(data, param)
        if not volume:
            return "no settings;\n", "", [], []
        volume = data[volume]
        if not isinstance(volume, dict):
            return "must contain settings formatted as {data: parameter, data: parameter ...};", "", [], []
        err, wrong_keys = check_keys(volume, self.volume_keys)
        for key in self.volume_keys:
            e = check_number(volume, key, 0, 100)
            if e:
                wrong_data_keys.append(key)
            err += e
        return "", err, wrong_data_keys, wrong_keys

    def check_deadtime(self, data: dict, param: str) -> Tuple[str, str, Sequence[str], Sequence[str]]:
        """
        checks if deadtime parameter is correct
        :param data: dict with settings
        :param param: key for dict
        :return: error message or ""
        """
        deadtime, error = check_existance(data, param)
        wrong_data_keys = []
        if error:
            return error, "", [], []
        warning, wrong_keys = check_keys(deadtime, self.deadtime_keys)
        for key in self.deadtime_keys:
            w = check_number(deadtime, key, 0, self.big_number)
            if w:
                wrong_data_keys.append(key)
            warning += w
        return error, warning, wrong_data_keys, wrong_keys


    def check_top_number(self, data: dict, param: str) -> Tuple[str, str, Sequence[str], Sequence[str]]:
        """
        checks number value in top level of dict
        :param data: dict with data
        :param param: key for number value
        :return: error message and empty string and lists to fit to common usage of checker functions
        """
        return check_number(data, param, 0, self.big_number), "", [], []

    def check_swing(self, data: dict, param: str) -> Tuple[str, str, Sequence[str], Sequence[str]]:
        """
        checks if swing parameters are correct, warning for unrial movement parameters
        :param data: dict with data
        :param param: key for swing data
        :return: error and warning or empty strings
        """
        swing, error = check_existance(data, 'swing')
        if error:
            return error, "", [], []
        wrong_data_keys = []
        warning, wrong_keys = check_keys(swing, self.swing_keys)
        w = check_number(swing, 'highw', 1, self.w_high)
        if w:
            wrong_data_keys.append('highw')
            warning += w
        w = check_number(swing, 'wpercent', 0, 100)
        if w:
            wrong_data_keys.append('wpercent')
            warning += w
        w = check_number(swing, 'circle', 100, 1000)
        if w:
            wrong_data_keys.append('circle')
            warning += w
        w = check_number(swing, 'circlew', 1, self.w_high)
        if w:
            wrong_data_keys.append('circlew')
            warning += w
        return "", warning, wrong_data_keys, wrong_keys

    def check_spin(self, data: dict, param: str) -> Tuple[str, str, Sequence[str], Sequence[str]]:
        """
        checks if spin parameters are correct, gives warning for unreal spin conditions and errors for other problems
        :param data: dict with spin settings
        :param spin: key to find spin data
        :return: error and warning messages or empty strings and lists of wrong keys and keys with wrong data
        """
        spin, error = check_existance(data, param)
        wrong_data_keys = list()
        if error:
            return error, "", [], []
        warning, wrong_keys = check_keys(spin, self.spin_keys)
        w = check_bool(spin, 'enabled')
        if warning:
            wrong_data_keys.append('enabled')
            warning += w
        w = check_number(spin, 'counter', 1, 10)
        if w:
            wrong_data_keys.append('counter')
            warning += w
        w = check_number(spin, 'w', 1, self.w_high)
        if w:
            wrong_data_keys.append('w')
            warning += w
        w = check_number(spin, 'circle', 100, 1000)
        if w:
            wrong_data_keys.append('counter')
            warning += w
        w = check_number(spin, 'wlow', self.w_low, self.w_high)
        if w:
            wrong_data_keys.append('counter')
            warning += w
        spin_w = get_value(spin, 'w')
        spin_w_low = get_value(spin, 'w_low')
        if spin_w and spin_w_low and spin_w_low >= spin_w:
            warning += "WLow should be less then W"
            wrong_data_keys.append('w')
            wrong_data_keys.append('w_low')
        return error, warning, wrong_data_keys, wrong_keys

    def check_clash(self, data: dict, param: str) -> Tuple[str, str, Sequence[str], Sequence[str]]:
        """
        checks if clash parameters are correct, gives warning for unreal spin conditions and errors for other problems
        :param data: dict with spin settings
        :param param: key with clash data
        :return: error and warning messages or empty strings
        """
        clash, error = check_existance(data, 'clash')
        if error:
            return error, "", [], []
        wrong_data_keys = list()
        warning, wrong_keys = check_keys(clash, self.clash_keys)
        w = check_number(clash, 'higha', self.a_low, self.a_high)
        if w:
            wrong_data_keys.append('higha')
            warning += w
        w =  check_number(clash, 'length', 0, self.big_number)
        if w:
            wrong_data_keys.append('length')
            warning += w
        w = check_number(clash, 'hitlevel', -self.big_number, -1)
        if w:
            wrong_data_keys.append('hitlevel')
            warning += w
        w = check_number(clash, 'loww', self.w_low, self.w_high)
        if w:
            wrong_data_keys.append('loww')
            warning += w
        return "", warning, wrong_data_keys, wrong_keys

    def check_stab(self, data: dict, param:str) -> Tuple[str, str, Sequence[str], Sequence[str]]:
        """
        checks if clash parameters are correct, gives warning for unreal spin conditions and errors for other problems
        :param data: dict with spin settings
        :param param: key for stab
        :return: error and warning messages or empty strings
        """
        stab, error = check_existance(data, 'stab')
        if error:
            return error, "", [], []
        warning, wrong_keys = check_keys(stab, self.stab_keys)
        wrong_data_keys = list()
        w = check_bool(stab, 'enabled')
        if w:
            warning += w
            wrong_data_keys.append('enabled')
        w = check_number(stab, 'higha', self.a_low, self.a_high)
        if w:
            warning += w
            wrong_data_keys.append('higha')
        w = check_number(stab, 'length', 0, self.big_number)
        if w:
            warning += w
            wrong_data_keys.append('length')
        w = check_number(stab, 'hitlevel', -self.big_number, -1)
        if w:
            warning += w
            wrong_data_keys.append('hitlevel')
        w = check_number(stab, 'loww', self.w_low, self.w_high)
        if w:
            warning += w
            wrong_data_keys.append('loww')
        w = check_number(stab, 'percent', 0, 100)
        if w:
            warning += w
            wrong_data_keys.append('percent')
        return error, warning, wrong_data_keys, wrong_keys

    def check_screw(self, data: dict, param: str) -> Tuple[str, str, Sequence[str], Sequence[str]]:
        """
        checks if screw parameters are correct, gives warning for unreal spin conditions and errors for other problems
        :param data: dict with spin settings
        :param param: key with screw data
        :return: error and warning messages or empty strings, list of wrong keys and list of wrong keys with data
        """
        screw, error = check_existance(data, 'screw')
        if error:
            return error, "", [], []
        warning, wrong_keys = check_keys(screw, self.screw_keys)
        wrong_data_key = list()
        w = check_bool(screw, 'enabled')
        if w:
            wrong_data_key.append('enabled')
            warning += w
        w = check_number(screw, 'highw', self.w_low, self.w_high)
        if w:
            wrong_data_key.append('highw')
            warning += w
        w = check_number(screw, 'loww', self.w_low, self.w_high)
        if w:
            wrong_data_key.append('loww')
            warning += w
        screw_loww = get_value(screw, 'loww')
        screw_highw = get_value(screw, 'highw')
        if screw_loww and screw_highw and screw_loww > screw_highw:
            warning += "LowW parameter must be less then HighW parameter"
            wrong_data_key.append('loww')
            wrong_data_key.append('highw')
        return "", warning, wrong_data_key, wrong_keys