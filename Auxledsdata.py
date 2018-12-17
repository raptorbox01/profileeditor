import json
from typing import Tuple, Optional, Any, List, Sequence

import IniToJson
import AuxChecker
import sys
from dataclasses import *


@dataclass
class AuxEffects:
    LedGroups: List['LedGroup'] = field(default_factory=list)
    # Sequencers: List["Sequencer"] = field(default_factory=list)



    def get_group_list(self)->Sequence[str]:
        """
        returns list of group names
        :return: list of groupnames for led groups
        """
        return [group.Name for group in self.LedGroups]

    def check_unique(self, group: 'LedGroup') -> bool:
        """
        checks if name is unique
        :param group: group to check
        :return:
        """
        return group.Name not in self.get_group_list()

    def add_group(self, name: str, leds_list: List[str])->Tuple[Optional['LedGroup'], str]:
        """
        adds group with selected name to LedGroups
        :param name: name of ledgroup
        :param leds_list: list of leds as str
        :return:
        """
        new_group: LedGroup = LedGroup(name, leds_list)
        verified_ledgroup = LedGroup.VerifyLedGroup(new_group)
        if not verified_ledgroup:
            return None, "Wrong symbols in LED group name (only latin letters, digits and _ available"
        is_unique = AuxEffects.check_unique(self, verified_ledgroup)
        if not is_unique:
            return None, "This group name is already used"
        self.LedGroups.append(verified_ledgroup)
        return verified_ledgroup, ""

    def save_to_file(self):
        pass


    @staticmethod
    def VerifyLength(src_json):
        if len(src_json.get("LedGroups", [])) == 0:
            print(
                """Warning!
                Your LedGroups seemingly contains 0 entries!
                """
            )
        if len(src_json.get("Sequencers", [])) == 0:
            print(
                """Warning!
                Your Sequencers seemingly contains 0 entries!
                """
            )

@dataclass
class LedGroup:
    Name: str
    Leds: List[str]

    def __repr__(self):
        return "%s: (%s LEDs)" % (self.Name, ', '.join(self.Leds))


    @staticmethod
    def CreationError(src_dict, e):
        print(
             """
                        Missing requirement in LedGroup description.
                        expecting: 
                        Name: somename, Leds[x,y,z]
                        got
                        {json_dumps(src_dict)}
                        """
        )

    @staticmethod
    def VerifyLength(src_json):
        if len(src_json.get("Leds", [])) == 0:
            print(
                """Warning!
                Your Leds seemingly contains 0 entries!
                """
            )

    @staticmethod
    def VerifyLedGroup(group)->Optional['LedGroup'] :
        """
        checks if LedGroup is correct
        :param group:
        :return:
        """
        valid = [ch.isalpha() or ch.isdigit() or ch == '_' for ch in group.Name]
        if all(valid):
            return group
        return None


class AuxEffect:

    def __init__(self):
        self.data = dict()
        self.sequencer_keys = ['config', 'sequence']

    def AddEffect(self, name: str):
        self.data[name] = list()

    def GetEffectsList(self):
        return self.data.keys()

    def GetUsedLedsList(self, effect: str):
        ledsused = list()
        try:
            sequencers = self.data[effect]
        except KeyError:
            print("No such effect % s" % effect)  # ToDo add logging
            return []
        for sequencer in sequencers:
            ledsused.extend(sequencer['Config'])
        return ledsused

    def GetJsonToFile(self, filename):
        text = json.dumps(self.data)
        text = text.replace(r'"', "")
        text = text[1:-1]
        f = open(filename, "w")
        f.write(text)

    def CreateSequencer(self, effect: str, leds: list):
        try:
            sequencers = self.data[effect]
        except KeyError:
            print("No such effect % s" % effect)  # ToDo add logging
        sequencers.append({"Config": leds, "Sequence": []})
        print(self.data)

    def CreateStep(self, effect: str, number: int, name: str, brightnesses: list, wait: int, smooth: int):
        try:
            sequence = self.data[effect][number]['Sequence']
            step = dict()
            if name:
                step['Name'] = name
            step['Brightness'] = brightnesses
            if wait > 0:
                step['Wait'] = wait
            if smooth > 0:
                step['Smooth'] = smooth
            sequence.append(step)
        except (KeyError, IndexError):
            print("Cannot add step to %i sequencer of %s effect" % (number, effect)) # ToDo add Logging
        print(self.data)

    def CreateRepeatStep(self, effect: str, number: int, startstep: str, count: str):
        try:
            sequence = self.data[effect][number]['Sequence']
            step = {'Repeat': {'StartingFrom': startstep}}
            if count != 'forever':
                count = int(count)
            step['Repeat']['Count'] = count
            sequence.append(step)
        except (KeyError, IndexError):
            print("Cannot add step to %i sequencer of %s effect" % (number, effect))  # ToDo add Logging
        print(self.data)

    def GetStepsList(self, effect: str, number: int):
        steps_list = list()
        try:
            sequence = self.data[effect][number]['Sequence']
            for step in sequence:
                if 'Name' in step.keys():
                    steps_list.append(step['Name'])
            return steps_list
        except (KeyError, IndexError):
            print("Cannot get steps of %i sequencer of %s effect" % (number, effect))  # ToDo add Logging
            return []

    def GetRepeatList(self, effect: str, number: int):
        repeat_list = list()
        try:
            sequence = self.data[effect][number]['Sequence']
            for step in sequence:
                if 'Repeat' in step.keys():
                    repeat_list.append(step['Repeat']['StartingFrom'])
            return repeat_list
        except (KeyError, IndexError):
            print("Cannot get steps of %i sequencer of %s effect" % (number, effect))  # ToDo add Logging
            return []

    def DeleteItem(self, item: str, parents: list):
        data = self.data
        for i in range(len(parents)):
            data = data[parents[i]]
        data.pop(item)
        print(self.data)

    def LoadDataFromText(self, text: str) -> Tuple[Optional[dict], Optional[str], str] :
        new_data, error = IniToJson.get_json(text)
        if error:
            return None, error, ""
        warning = ""
        Checker = AuxChecker.AuxChecker()
        try:
            wrong_effects = []
            for effect in new_data.keys():

                # check if effect data is a list
                if not isinstance(new_data[effect], list):
                    wrong_effects.append(effect)
                    warning += "%s effect data is wrong, effect is not loaded.\n" % effect
                    continue
                leds_used = []

                for sequencer in new_data[effect]:
                    i_seq = new_data[effect].index(sequencer) + 1

                    # check if sequencer is a dict
                    if not isinstance(sequencer, dict):
                        warning += "'%s' effect, %i sequencer: Wrong sequencer data, " \
                                   "sequencer is not loaded.\n" % (effect, i_seq)
                        new_data[effect].remove(sequencer)
                        continue

                    # check sequencer keys and remove wrong
                    wrong_keys = []
                    for key in sequencer.keys():
                        if key.lower() not in self.sequencer_keys:
                            warning += "'%s' effect, %i sequencer: Wrong sequencer data, " \
                                       "sequencer is not loaded.\n" % (effect, i_seq)
                            wrong_keys.append(key)
                    for key in wrong_keys:
                        sequencer.pop(key)

                    # check config part of sequencer
                    error, leds_count, leds_used = Checker.check_config(sequencer, leds_used)
                    if error:
                        warning += "'%s' effect, %i sequencer: %s " \
                                 "This sequencer is not loaded.\n" % (effect, i_seq, error)
                        new_data[effect].remove(sequencer)
                        continue

                    # check sequence part of sequencer
                    error = Checker.check_sequence(sequencer)
                    if error:
                        warning += "Error: '%s' effect, %i sequencer: %s " \
                                   "Step for this sequencer are not loaded.\n" % (effect, i_seq, error)
                        sequencer['Sequence'] = {}
                        continue
                    namelist = []
                    for step in sequencer['Sequence']:
                        i_step = sequencer['Sequence'].index(step) + 1

                        # check if step is a dictionary
                        if not isinstance(step, dict):
                            warning += "Error: '%s' effect, %i sequencer, %i step):" \
                                       " step data is incorrect, step is skipped.\n" % (effect, i_seq, i_step)
                            sequencer['Sequence'].remove(step)
                            continue

                        # check if step keys are correct (no wrong steps, brightness or repeat or wait in step)
                        error, w, wrong_keys,  = Checker.check_step_keys(step)
                        if error:
                            warning += "Error: '%s' effect, %i sequencer, %i step): %s " \
                                       "This step is not loaded.\n" % (effect, i_seq, i_step, error)
                            sequencer['Sequence'].remove(step)
                            continue
                        if wrong_keys:
                            warning += "Error: '%s' effect, %i sequencer, %i step): " \
                                       "%s this data is not loaded.\n" % (effect, i_seq, i_step, w)
                        for key in wrong_keys:
                            step.pop(key)

                        if 'Name' in step.keys():
                            if not isinstance(step['Name'], str):
                                warning += "Error: '%s' effect, %i sequencer, %i step): " \
                                           "wrong name data, name is skipped.\n" % (effect, i_seq, i_step)
                                step.pop('Name')
                            else:
                                if step['Name'] in namelist:
                                   warning += "Error: '%s' effect, %i sequencer, %i step): " \
                                              "name already used, name is skipped.\n" % (effect, i_seq, i_step)
                                   step.pop('Name')
                                else:
                                   namelist.append(step['Name'])

                        # check step brightness correct
                        error, brightness = Checker.check_brightness(step, leds_count)
                        if error:
                            warning += "Error: '%s' effect, %i sequencer, %i step: %s " \
                                       "step brightness is skipped.\n" % (effect, i_seq, i_step, error)
                            if brightness:
                                step.pop(brightness)

                        # check wait parameters is correcr
                        error = Checker.check_wait(step)
                        if error:
                            warning += "Error: '%s' effect, %i sequencer, %i step: %s " \
                                       "step wait is skipped.\n" % (effect, i_seq, i_step, error)
                            step.pop('Wait')

                        # check if smooth parameter is correct
                        error, smooth = Checker.check_smooth(step)
                        if error:
                            warning += "Error: '%s' effect, %i sequencer, %i step: %s " \
                                       "step smooth is skipped.\n " % (effect, i_seq, i_step, error)
                            step.pop(smooth)

                        # check repeat
                        error = Checker.check_repeat(step, namelist)
                        if error:
                            warning += "Error: '%s' effect, %i sequencer, %i step: %s. " \
                                       "This repeat step is not loaded\n " % (effect, i_seq, i_step, error)
                            sequencer['Sequence'].remove(step)

            # remove effects with not list data
            for effect in wrong_effects:
                new_data.pop(effect)
            return new_data, None, warning
        # for everything unexpected
        except Exception:
            e = sys.exc_info()[1]
            return None, e.args[0], ""
