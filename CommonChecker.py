from CommonChecks import *



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

    def common_check_keys(self, data:dict) -> str:
        """

        :param data:
        :param keys:
        :return:
        """
        return check_keys(data, self.common_keys)

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
            return error, "", []
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


    def check_volume(self, data: dict) -> (str, str, [str], [str]):
        """
        checks if folume parameter is correct
        :param data: dict with wolume settings
        :return: error message or ""
        """
        wrong_data_keys = []
        volume = get_real_key(data, 'volume')
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