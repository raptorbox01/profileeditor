from CommonChecks import *
from typing import Tuple, Sequence


class ProfileChecker:
    effects_keys = ['PowerOn', 'AfterWake', 'PowerOff', 'Flaming', 'Blade2', 'Lockup', 'Stab', 'Clash', 'Blaster',
                    'Workingmode', 'Flickering']
    afterwake_keys = ['auxleds']
    workingmode_keys = ['color', "flaming", "flickeringalways", "auxleds"]
    on_off_keys = ['blade', 'auxleds']
    flaming_keys = ['size', 'speed', 'delay_ms', "colors", "auxleds"]
    blade2_flaming_keys = ['size', 'speed', 'delay_ms', "colors", "auxleds", "alwayson"]
    flickering_keys = ['time', 'brightness', "auxleds"]
    blade2_flickering_keys = ['time', 'brightness', "auxleds", "alwayson"]
    move_keys = ['color', 'duration_ms', 'sizepix', 'auxleds']
    lockup_keys = ['flicker', 'flashes', 'auxleds']
    lockup_flicker_keys = ['color', 'time', 'brightness']
    lockup_flashes_keys = ['period', 'color', 'duration_ms', 'sizepix']
    blade2_keys = ['flaming', 'workingmode', 'flickering', 'delaybeforeon', 'indicateblasterclashlockup']
    big_number = 9999
    connection = {'PowerOn': on_off_keys, 'AfterWake': afterwake_keys, 'PowerOff': on_off_keys,
                  'WorkingMode': workingmode_keys, 'Flaming': flaming_keys, 'Flickering': flickering_keys,
                  'Stab': move_keys, 'Clash': move_keys, 'Blaster': move_keys, 'Lockup': lockup_keys,
                  'Blade2': blade2_keys}
    blade2_connection = {'Flaming': blade2_flaming_keys, 'Flickering': blade2_flickering_keys, 'WorkingMode': 'Color'}

    def get_key(self, data: dict, key: str):
        """
        gets case insensitive key
        :param key: key to find
        :param data: dict with data
        :return:
        """
        for new_key in data.keys():
            if key.lower() == new_key.lower():
                return new_key
        return ""

    def check_auxleds(self, data: dict) -> str:
        """
        checks if auxledeffect string is correct
        :param data: dict with settings data
        :return: error message or  empty string
        """
        auxleds = get_real_key(data, "auxleds")
        if auxleds:
            if not isinstance(data[auxleds], list):
                return "auxleds effect must be formatted as [Effect1, Effect2];\n"
        return ""

    def check_afterwake(self, data: dict) -> Tuple[str, str]:
        """
        function chacks afterwake effect and returns error message or empty string
        :param data: dict with effect settings
        :return: error and warning messages or empty strings
        """
        afterwake, error = check_existance(data, 'afterwake')
        if error:
            return error, ""
        warning = self.check_auxleds(afterwake)
        error += check_keys(afterwake, ['auxleds'])
        return error, warning

    def check_poweron(self, data: dict) -> (str, str):
        """
        checks poweron effect
        :param data: data wit effect settings
        :return: error and warning message or ""
        """
        poweron, error = check_existance(data, 'poweron')
        if error:
            return error, ''
        warning = self.check_auxleds(poweron)
        error += check_keys(poweron, self.on_off_keys)
        blade, error_blade = check_existance(poweron, 'blade')
        if blade:
            error_blade += check_number(blade, "speed", 0, self.big_number)
            error_blade += check_keys(blade, ['speed'])
        if error_blade:
            error += "Blade: " + error_blade
        return error, warning

    def check_workingmode(self, data: dict) -> (str, str):
        """
        checks if working mode settings are correct (all parameters exist and are of correct type and meaning,
        flaming effect exists if used
        flaming and flickering keys absent produce warning, other keys - error
        :param data: dict wit settings
        :return: error and warning messages (or empty strings)
        """
        workingmode, error = check_existance(data, 'workingmode')
        if error:
            return error, ""
        error += check_keys(workingmode, self.workingmode_keys)
        error += check_color(workingmode)
        error += check_bool(workingmode, 'flaming')
        error += check_bool(workingmode, 'flickeringalways')
        warning = self.check_auxleds(workingmode)
        return error, warning

    def check_poweroff(self, data: dict) -> (str, str):
        """
        check poweroff settings (if setting for blade (speed, direction) and auxeffect are present and correct
        :param data: dict with poweroff settings
        :return: error and warning message or empty strings
        """
        poweroff, error = check_existance(data, 'poweroff')
        if error:
            return error, ""
        error += check_keys(poweroff, self.on_off_keys)
        blade, error_blade = check_existance(poweroff, 'blade')
        if blade:
            error_blade += check_number(blade, 'speed', 0, self.big_number)
            error_blade += check_bool(blade, 'moveforward')
            error_blade += check_keys(blade, ['speed', 'moveforward'])
        warning = self.check_auxleds(poweroff)
        if error_blade:
            error += 'Blade: ' + error_blade
        return error, warning

    def check_flaming(self, data: dict, keylist: list, led_number: int) -> (str, str):
        """
        checks if flaming settings are correct
        :param data: dict with flaming settings
        :param keylist: list with keys for flaming effect
        :param led_number: number of leds in blade
        :return: error and warning messages or empty strings
        """
        flaming, error = check_existance(data, 'flaming')
        if error:
            return error, ""
        error = check_keys(flaming, keylist)
        error += check_min_max_parameter(flaming, "size", 0, led_number)
        error += check_min_max_parameter(flaming, "speed", 0, self.big_number)
        error += check_min_max_parameter(flaming, "delay_ms", 0, self.big_number)
        error += check_color_from_list(flaming)
        warning = self.check_auxleds(flaming)
        return error, warning

    def check_flickering(self, data: dict, keylist: list) -> (str, list):
        """
        checks if flickering settings are cortect
        :param data: dict with flickering setting
        :param keylist: list of keys for flickering setting
        :return: error and warning message or empty strings
        """
        flickering, error = check_existance(data, 'flickering')
        if error:
            return error, ""
        error += check_keys(flickering, keylist)
        error += check_min_max_parameter(flickering, "time", 0, self.big_number)
        error += check_min_max_parameter(flickering, "brightness", 0, 100)
        warning = self.check_auxleds(flickering)
        return error, warning

    def check_movement(self, data: dict, leds_number: int, key: str) -> (str, str):
        """
        checks if blaster/clash/stab effect is correct
        :param data: dict with settings
        :param key: type of movement (blaster/clash/stab)
        :param leds_number: number or lades in blade
        :return: error or warning messages or empty strings
        """
        move, error = check_existance(data, key.lower())
        if error:
            return error, ""
        error += check_keys(move, self.move_keys)
        error += check_number(move, "duration_ms", 0, self.big_number)
        error += check_number(move, "sizepix", 0, leds_number)
        error += check_color(move)
        warning = self.check_auxleds(move)
        return error, warning

    def check_flicker(self, data: dict) -> str:
        """
        checks flicker settings for lockup parameter
        :param data: dict with settings
        :return: error or empty message
        """
        flicker, error = check_existance(data, 'flicker')
        if error:
            return error
        error, wrong_keys = check_keys(flicker, self.lockup_flicker_keys)
        error += check_color(flicker)
        error += check_min_max_parameter(flicker, 'time', 0, self.big_number)
        error += check_min_max_parameter(flicker, 'brightness', 0, 100)
        return error

    def check_flashes(self, lockup: dict, leds_number: int) -> str:
        """
        checks flashes settings for lockup parameter
        :param lockup: dict with settings
        :param leds_number: number of leds
        :return: error or empty message
        """
        flashes, error = check_existance(lockup, 'flashes')
        if error:
            return error
        error, wrong_keys = check_keys(flashes, self.lockup_flashes_keys)
        error += check_color(flashes)
        error += check_min_max_parameter(flashes, "period", 0, self.big_number)
        error += check_number(flashes, 'duration_ms', 0, self.big_number)
        error += check_number(flashes, 'sizepix', 0, leds_number)
        return error

    def check_lockup(self, data: dict, leds_number: int) -> (str, str):
        """
        checks of lockup effect settins are correct
        :param data: dict with data
        :param leds_number: number of leds in blade
        :return: error and warning messages or empty strings
        """
        lockup, error = check_existance(data, 'lockup')
        if error:
            return error, ""
        error += check_keys(lockup, self.lockup_keys)
        warning = self.check_auxleds(lockup)
        flicker_error = self.check_flicker(lockup)
        if flicker_error:
            error += 'Flicker: ' + flicker_error
        flashes_error = self.check_flashes(lockup, leds_number)
        if flashes_error:
            error += 'Flashes: ' + flashes_error
        return error, warning

    def check_blade2(self, data: dict, leds_number: int) -> (str, str):
        """
        checks if blade2 settings are correct
        :param data: dict with settings of blade2
        :param leds_number: number of leds in blade
        :return:
        """
        warning = ""
        blade2, error = check_existance(data, 'blade2')
        if blade2:
            error, wrong_keys = check_keys(blade2, self.blade2_keys)
            flickering = get_real_key(blade2, "flickering")
            if flickering:
                error_flickering, warning_flickering = self.check_flickering(blade2, self.blade2_flickering_keys)
                flickering = blade2[flickering]
                if isinstance(flickering, dict):
                    error_flickering += check_bool(flickering, "alwayson")
                if error_flickering:
                    error += "flickering: %s" % error_flickering
                if warning_flickering:
                    warning += "flickering: %s" % warning_flickering
            flaming = get_real_key(blade2, "flaming")
            if flaming:
                error_flaming, warning_flaming = self.check_flaming(blade2, self.blade2_flaming_keys, leds_number)
                flaming = blade2[flaming]
                if isinstance(flaming, dict):
                    error_flaming += check_bool(flaming, "alwayson")
                if error_flaming:
                    error += "flaming: %s" % error_flaming
                if warning_flaming:
                    warning += "flaming: %s" % warning_flaming
            error += check_number(blade2, "delaybeforeon", 0, self.big_number)
            workingmode, error_workingmode = check_existance(blade2, 'workingmode')
            if workingmode:
                error_workingmode = check_keys(workingmode, ['color', 'auxledseffect'])
                error_workingmode += check_color(workingmode)
                warning_workingmode = self.check_auxleds(workingmode)
                if warning_workingmode:
                    warning += "working mode: %s" % warning_workingmode
            if error_workingmode:
                error += "working mode: %s" % error_workingmode
            error += check_bool(blade2, 'indicateblasterclashlockup')
        return error, warning


"""
    for profile in data.keys():
        if not isinstance(data[profile], dict):
            print("Wrong settings format for profile %s;" % profile)
            continue
        errors = {err: "" for err in effects_keys}
        warnings = {warn: "" for warn in effects_keys}
        error = check_keys(data[profile], [key.lower() for key in effects_keys])
        if error:
            print(error)
        errors['AfterWake'], warnings['Afterwake'] = check_afterwake(data[profile], aux_list)
        errors['PowerOn'], warnings['PowerOn'] = check_poweron(data[profile], aux_list)
        errors['WorkingMode'], warnings['WorkingMode'] = check_workingmode(data[profile], aux_list)
        errors['PowerOff'], warnings['PowerOff'] = check_poweroff(data[profile], aux_list)
        errors['Flaming'], warnings['Flaming'] = check_flaming(data[profile], flaming_keys, leds_number, aux_list)
        errors['Flickering'], warnings['Flickering'] = check_flickering(data[profile], flickering_keys, aux_list)
        errors['Blaster'], warnings['Blaster'] = check_movement(data[profile], leds_number, "Blaster", aux_list)
        errors['Clash'], warnings['Clash'] = check_movement(data[profile], leds_number, "Clash", aux_list)
        errors['Stab'], warnings['Stab'] = check_movement(data[profile], leds_number, "Stab", aux_list)
        errors['Lockup'], warnings['Lockup'] = check_lockup(data[profile], leds_number, aux_list)
        errors['Blade2'], warnings['Blade2'] = check_blade2(data[profile], leds_number, aux_list)
        for key in errors.keys():
            if errors[key]:
                print("Error: %s profile %s effect:\n%s" % (profile, key, errors[key].strip()))
            if warnings[key]:
                print("Warning: %s profile %s effect:\n%s" % (profile, key, warnings[key].strip()))"""
