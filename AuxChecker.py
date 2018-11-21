from CommonChecks import *
leds_copy_list = ['copyred', 'copyblue', 'copygreen']

class AuxChecker:
    step_keys = ['repeat', 'wait', 'brightness', 'smooth', 'name']

    def check_config(self, sequencer: dict, leds_used: list) -> (str, int, list):
        """
        checks if sequencer config exists, is not empty, is correct
        (leds are not conflicting with used leds, leds are selected properly)
        :param sequencer: dictionary with sequencer data
        :param leds_used: list of used leds
        :return: error text or empty string
        """
        error = ""
        config = get_real_key(sequencer, "config")
        if not config:
            return "no config string with leds list;", 0, leds_used
        if not isinstance(sequencer[config], list):
            return "config parameter must be list of LEDS (for example [Led1, Led2]);", 0, leds_used
        leds_count = len(sequencer[config])
        if leds_count == 0:
            return "0 LEDs selected", 0, leds_used
        incorrect_leds = [led for led in sequencer[config] if
                          led.lower() not in ['led1', 'led2', 'led3', 'led4', 'led5', 'led6', 'led7', 'led8']]
        if incorrect_leds:
            error += "incorrect led value;\n"
        for led in sequencer[config]:
            if led in leds_used:
                error += "%s: this led is already used in other sequencer for this effect;\n" % led
            else:
                leds_used.append(led)
        return error.strip(), leds_count, leds_used


    def check_sequence(self, sequencer: dict) -> str:
        """
        checks is sequence exists, if sequences are an array and this array is not empty
        :param sequencer: sequencer dict
        :return: error empty string
        """
        sequence = get_real_key(sequencer, "sequence")
        if not sequence or not isinstance(sequencer[sequence], list):
            return "no steps"
        return ""

    def check_step_keys(self, step: dict) -> str:
        """
        check if step keys are corrent (no incorrect keys, and each step is step or wait or repeat)
        :param step: dict with step data
        :return: error message or empty string
        """
        error = ""
        repeat = get_real_key(step, "repeat")
        brightness = get_real_key(step, "brightness")
        wait_key = get_real_key(step, "wait")
        if not repeat and not brightness and not wait_key:
            error = "each step must contain brightness or repeat or wait;\n"
        warning, wrong_keys = check_keys(step, self.step_keys)
        return error.strip(), warning, wrong_keys

    def check_brightness(self, step: dict, leds_count: int) -> (str, str):
        """
        check if brightness settings are correct (correct number of leds, brightness is not negative number or copy value
        :param step: dict with step data
        :param leds_count: number of leds configurated for this step
        :return:
        """
        brightness = get_real_key(step, "brightness")
        if brightness:
            brightness = step[brightness]
            if not isinstance(brightness, list):
                return "Brightness must be a list of leds", get_real_key(step, "brightness")
            if len(brightness) != leds_count:
                return "incorrect leds number", brightness
            for led in brightness:
                if isinstance(led, int):
                    if led < 0 or led > 100:
                        return "%i led brightness is not correct (expect value from 0 to 100 inclusively)" \
                               % (brightness.index(led) + 1), get_real_key(step, "brightness")
                else:
                    if led.lower() not in leds_copy_list:
                        return "%i led is incorrect: use 0...100 or one of CopyRed, CopyBlue, CopyGreen values" \
                               % (brightness.index(led) + 1), get_real_key(step, "brightness")
        return "", brightness