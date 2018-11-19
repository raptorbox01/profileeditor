leds_list = ["Led1", "Led2", "Led3", "Led4", "Led5", "Led6", "Led7", "Led8"]
config_name = 'Config'
seq_name = "Sequence"

def get_leds_from_config(config: str) -> list:
    """
    gets leds list from config string
    :param config: string with config
    :return: leds list
    """
    return config.split(", ")

def get_config_name_from_leds(leds: list) -> str:
    """
    creates name for config string using leds names
    :param leds: list of leds
    :return: config name
    """
    return ', '.join(leds)

def get_step_name(name: str, brightnesses: list, wait: int, smooth: int) -> str:
    """
    gets step name for item tree using parameters values
    :param name: name of step
    :param brightnesses: list of leds brightnesses
    :param wait: wait value
    :param smooth: smooth value
    :return: parameter string
    """
    step_text = []
    if name:
        step_text.append('Name: %s' % name)
    brightnesses = list(map(str, brightnesses))
    brightnesses = ', '.join(brightnesses)
    step_text.append("Brightness: [%s]" % brightnesses)
    if wait > 0:
        step_text.append('Wait: %i' % wait)
    if smooth > 0:
        step_text.append('Smooth: %i' % smooth)
    step_text = ', '.join(step_text)
    return step_text


def get_repeat_name(startstep: str, count: str)->str:
    """
    create name for repeat step using parameters
    :param startstep: name of step to start repeat
    :param count: number of repeats
    :return: step name
    """
    return "Repeat: StartFrom: %s, Count: %s" % (startstep, count)

def get_currrent_step_name (name: str) -> str:
    """
    gets step name from name with parameters
    :param name: name wit parameters
    :return: step_name
    """
    text_items = name.split(', ')
    step_name = ""
    for item in text_items:
        words = item.split(": ")
        if words[0] == 'Name':
            step_name = words[1]
    return step_name