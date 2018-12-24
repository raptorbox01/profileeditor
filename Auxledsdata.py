import json
from typing import Tuple, Optional, List, Sequence, Union, Dict

import IniToJson
import AuxChecker
import sys
from dataclasses import *


@dataclass
class AuxEffects:
    LedGroups: List['LedGroup'] = field(default_factory=list)
    Sequencers: List['Sequencer'] = field(default_factory=list)

    def get_group_list(self)->Sequence[str]:
        """
        returns list of group names
        :return: list of groupnames for led groups
        """
        return [group.Name for group in self.LedGroups]

    def get_seq_names(self) -> List[str]:
        """
        returns list of Sequencer names
        :return:
        """
        return [seq.Name for seq in self.Sequencers]

    def check_unique(self, data: Union['LedGroup', 'Sequencer', 'Step'], datatype: str, seq: Optional['Sequencer']) \
            -> bool:
        """
        checks if name is unique
        :param data data to check
        :param datatype: LedGroup or Sequencer
        :param seq: sequencer for step analyses
        :return:
        """
        if datatype == 'LedGroup':
            return data.Name not in self.get_group_list()
        elif datatype == 'Sequencer':
            return data.Name not in self.get_seq_names()
        else:
            return data.Name not in seq.get_steps_names()

    def get_seq_by_name(self, name: str)-> Optional['Sequencer']:
        """
        gets sequencer by its name
        :param name: name of Sequencer
        :return: Sequencer
        """
        for seq in self.Sequencers:
            if seq.Name == name:
                return seq
        return None

    def get_group_by_name(self, name: str)->Optional['Group']:
        """
        returns a group using its name
        :param name: group name
        :return: Group
        """
        for group in self.LedGroups:
            if group.Name == name:
                return group
        return None

    def add_group(self, name: str, leds_list: List[str])->Tuple[Optional['LedGroup'], str]:
        """
        adds group with selected name to LedGroups
        :param name: name of ledgroup
        :param leds_list: list of leds as str
        :return:
        """
        new_group: LedGroup = LedGroup(name, leds_list)
        verified_ledgroup = LedGroup.verify_led_group(new_group)
        if not verified_ledgroup:
            return None, "Wrong symbols in LED group name (only latin letters, digits and _ available"
        is_unique = AuxEffects.check_unique(self, verified_ledgroup, 'LedGroup', None)
        if not is_unique:
            return None, "This group name is already used"
        self.LedGroups.append(verified_ledgroup)
        return verified_ledgroup, ""

    def delete_group_and_enable_leds(self, description: str)->Optional[List[str]]:
        """
        deletes group from data and return it leds to make them available again
        :param description:
        :return:
        """
        name = LedGroup.get_name(description)
        for seq in self.Sequencers:
            if seq.Group == name:
                return None
        group_for_delete = self.get_group_by_name(name)
        if group_for_delete:
            self.LedGroups.remove(group_for_delete)
            return group_for_delete.Leds
        return None

    def create_sequence(self, group_name: str, name: str):
        """
        creates new sequencer for group_name with name name
        :param group_name: group to add sequencer
        :param name: name of new sequencer
        :return:
        """
        group_name: str = LedGroup.get_name(group_name)
        new_seq: Sequencer = Sequencer(name, group_name, [])
        verified_seq = Sequencer.verify_sequencer(new_seq)
        if not verified_seq:
            return None, "Wrong symbols in Sequencer name (only latin letters, digits and _ available"
        is_unique = AuxEffects.check_unique(self, verified_seq, "Sequencer", None)
        if not is_unique:
            return None, "This Sequencer name is already used"
        self.Sequencers.append(verified_seq)
        return verified_seq, ""

    def delete_sequence(self, name: str):
        """
        deletes sequencer
        :param name: description of Sequencer
        :return:
        """
        seq_name: str = Sequencer.get_name(name)
        seq_to_delete = self.get_seq_by_name(seq_name)
        if seq_to_delete:
            self.Sequencers.remove(seq_to_delete)
        else:
            pass # to do logging

    def get_led_list(self, name: str)-> Optional[List[str]]:
        """
        finds leds list for selected sequencer name
        :param name: sequencer description
        :return: list of led names
        """
        seq_name: str = Sequencer.get_name(name)
        for seq in self.Sequencers:
            if seq.Name == seq_name:
                group = seq.Group
        group = self.get_group_by_name(group)
        if group:
            return group.Leds
        return None

    def create_step(self, seq_descr: str, name: str, brigthnesses: List[Union[str, int]], smooth: int, wait: int) \
            -> Tuple[Optional['Step'], str]:
        """
        creates step for selected sequencer with selected params
        :param seq_descr: name of sequencer
        :param name: name of step
        :param brigthnesses:  list of step brightnesses
        :param smooth: step smooth
        :param wait: step wait
        :return: step or None and error message
        """
        seq_name: str = Sequencer.get_name(seq_descr)
        new_step: Step = Step(Name=name, Brightness=brigthnesses, Wait=wait, Smooth=smooth)
        verified_step = Step.verify_step(new_step)
        if not verified_step:
            return None, "Wrong symbols in Step name (only latin letters, digits and _ available"
        current_seq = self.get_seq_by_name(seq_name)
        is_unique = AuxEffects.check_unique(self, verified_step, "Step", current_seq)
        if not is_unique:
            return None, "This Step name is already used"
        current_seq.Sequence.append(verified_step)
        return verified_step, ""

    def delete_step(self, step_descr: str, seq_descr: str):
        """
        delete described step for described sequencer
        :param step_descr: described step
        :param seq_name: described sequencer
        :return:
        """
        step_name = Step.get_name(step_descr)
        seq = self.get_seq_by_name(Sequencer.get_name(seq_descr))
        for step in seq.Sequence:
            if isinstance(step, Step) and step.Name == step_name:
                seq.Sequence.remove(step)

    def save_to_file(self, filename: str):
        """
        save data as a preudojson (no quotes) to filename file
        :param filename: name of file
        :return:
        """
        prepare = asdict(self)
        text = json.dumps(prepare)
        text = text.replace(r'"', "")
        text = text[1:-1]
        f = open(filename, "w")
        f.write(text)

    # @staticmethod
    # def VerifyLength(src_json):
    #   if len(src_json.get("LedGroups", [])) == 0:
    #        print(
    #            """Warning!
    #             Your LedGroups seemingly contains 0 entries!
    #             """
    #         )
    #     if len(src_json.get("Sequencers", [])) == 0:
    #         print(
    #             """Warning!
    #             Your Sequencers seemingly contains 0 entries!
    #             """
    #         )
    #


@dataclass
class LedGroup:
    Name: str
    Leds: List[str]

    def __str__(self):
        return "%s (%s)" % (self.Name, ', '.join(self.Leds))

    @staticmethod
    def get_name(descr: str)->str:
        """
        gets name of group from string formatted as str for this class
        :param descr: description
        :return: name
        """
        return descr.split()[0]

    # @staticmethod
    # def CreationError(src_dict, e):
    #     print(
    #          """
    #                     Missing requirement in LedGroup description.
    #                     expecting:
    #                     Name: somename, Leds[x,y,z]
    #                     got
    #                     {json_dumps(src_dict)}
    #                     """
    #     )

    # @staticmethod
    # def VerifyLength(src_json):
    #     if len(src_json.get("Leds", [])) == 0:
    #         print(
    #             """Warning!
    #             Your Leds seemingly contains 0 entries!
    #             """
    #         )

    @staticmethod
    def verify_led_group(group)->Optional['LedGroup']:
        """
        checks if LedGroup is correct
        :param group: group name to validate
        :return:
        """
        valid = [ch.isalpha() or ch.isdigit() or ch == '_' for ch in group.Name]
        if all(valid):
            return group
        return None


@dataclass
class Sequencer:
    Name: str
    Group: str
    Sequence: List[Union['Step', 'Repeater']] = field(default_factory=list)

    def __str__(self):
        return "%s (%s LED group)" % (self.Name, self.Group)

    def get_steps_names(self) -> List[str]:
        """
        gets step names for selected Sequencer
        :param seq: Sequencer
        :return: step names
        """
        return [step.Name for step in self.Sequence if isinstance(step, Step)]

    def get_repeat_steps_names(self) -> List[str]:
        """
        gets repeat step names for selected Sequencer
        :param seq: Sequencer
        :return: repeat step names
        """
        return [step.Start for step in self.Sequence if isinstance(step, Repeater)]

    def get_max_step_number(self):
        """
        get max used step number for steps with default name Step1...
        :return: step number
        """
        max_num = 0
        for step in self.Sequence:
            if isinstance(step, Step) and 'step' in step.Name.lower():
                tail = step.Name.lower().replace('step', '')
                if tail.isdigit():
                    num = int(tail)
                    max_num = max(max_num, num)
        return max_num


    @staticmethod
    def get_name(descr: str) -> str:
        """
        return sequencer name
        :param descr: sequencer description
        :return: sequencer name
        """
        return descr.split(' (')[0]

    @staticmethod
    def verify_sequencer(seq: 'Sequencer') -> Optional['Sequencer']:
        """
        checks if LedGroup is correct
        :param seq: Sequencer object
        :return:
        """
        valid = [ch.isalpha() or ch.isdigit() or ch == '_' for ch in seq.Name]
        if all(valid):
            return seq
        return None

    # @staticmethod
    # def CreationError(src_dict, e):
    #     print(
    #         f"""
    #                 Missing requirement in Sequencer description.
    #                 expecting:
    #                 Name: somename, Group: somegroup, Steps: [...
    #                 got
    #                 {json_dumps(src_dict)}
    #                 """
    #     )
    #
    # def RemoveDuplicates(self):
    #     names: Dict[str, int] = dict()
    #     for step in self.Sequence:
    #         if isinstance(step, Repeater):
    #             continue
    #         name = step.Name
    #         if not isinstance(step, Repeater) and (name != ''):
    #             if name not in names:
    #                 names[name] = 1
    #             else:
    #                 names[name] += 1
    #     for step in self.Sequence:
    #         if isinstance(step, Repeater):
    #             continue
    #         name = step.Name
    #         if name and (names[name] > 1):
    #             names[name] -= 1
    #             step.Name = name + f"({names[name]})"
    #     pass


@dataclass
class Step:
    Brightness: List[Union[int, str]]
    Name: str = ""
    Wait: int = 0
    Smooth: int = 0

    def __str__(self):
        return "%s ([%s], Wait: %i, Smooth: %i)" % (self.Name, ", ".join(list(map(str, self.Brightness))),
                                                             self.Wait, self.Smooth)

    @staticmethod
    def get_name(descr: str) -> str:
        """
        return sequencer name
        :param descr: sequencer description
        :return: sequencer name
        """
        return descr.split(' (')[0]

    @staticmethod
    def verify_step(step: 'Step') -> Optional['Step']:
        """
        checks if Step is correct
        :param step: Step object
        :return:
        """
        valid = [ch.isalpha() or ch.isdigit() or ch == '_' for ch in step.Name]
        if all(valid):
            return step
        return None


    # @staticmethod
    # def CreationError(src_dict, e):
    #     print(
    #         f"""
    #         Missing requirement in Step description.
    #         expecting:
    #         Brightness: [...], [Smooth: x,] [Wait :y]
    #         got
    #         {json_dumps(src_dict)}
    #         """
    #     )


@dataclass
class Repeater:
    Start: str
    Count: Union[int, str]



sequencer_keys = ["config", "sequence"]


def DataLoad(json: Dict) -> AuxEffects:
    auxleds = AuxEffects()
    AuxEffects.VerifyLength(json)

    for led in json.get("LedGroups", []):
        try:
            ledgroup = LedGroup(**led)
            auxleds.LedGroups.append(ledgroup)
            LedGroup.VerifyLength(led)
        except Exception as e:
            LedGroup.CreationError(led, e)
    for sequencer in json.get("Sequencers", []):
        try:
            name, group, sequence = sequencer.values()
            auxleds.Sequencers.append(Sequencer(Name=name, Group=group))
        except Exception as e:
            Sequencer.CreationError(sequencer, e)

        for step in sequencer.get("Sequence", []):
            current_sequence = auxleds.Sequencers[-1].Sequence
            if "Repeat" not in step:
                try:
                    current_sequence.append(Step(**step))
                except Exception as e:
                    Step.CreationError(step, e)
            else:
                current_sequence.append(Repeater(**step))
            auxleds.Sequencers[-1].RemoveDuplicates()
    return auxleds


def ValidateAux(data: AuxEffects) -> Tuple[Optional[AuxEffects], Optional[str], str]:
    # new_data, error = IniToJson.get_json(text)
    error = None
    new_data = data
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
                    warning += (
                            "'%s' effect, %i sequencer: Wrong sequencer data, "
                            "sequencer is not loaded.\n" % (effect, i_seq)
                    )
                    new_data[effect].remove(sequencer)
                    continue

                # check sequencer keys and remove wrong
                wrong_keys = []
                for key in sequencer.keys():
                    if key.lower() not in sequencer_keys:
                        warning += (
                                "'%s' effect, %i sequencer: Wrong sequencer data, "
                                "sequencer is not loaded.\n" % (effect, i_seq)
                        )
                        wrong_keys.append(key)
                for key in wrong_keys:
                    sequencer.pop(key)

                # check config part of sequencer
                error, leds_count, leds_used = Checker.check_config(
                    sequencer, leds_used
                )
                if error:
                    warning += (
                            "'%s' effect, %i sequencer: %s "
                            "This sequencer is not loaded.\n" % (effect, i_seq, error)
                    )
                    new_data[effect].remove(sequencer)
                    continue

                # check sequence part of sequencer
                error = Checker.check_sequence(sequencer)
                if error:
                    warning += (
                            "Error: '%s' effect, %i sequencer: %s "
                            "Step for this sequencer are not loaded.\n"
                            % (effect, i_seq, error)
                    )
                    sequencer["Sequence"] = {}
                    continue
                namelist = []
                for step in sequencer["Sequence"]:
                    i_step = sequencer["Sequence"].index(step) + 1

                    # check if step is a dictionary
                    if not isinstance(step, dict):
                        warning += (
                                "Error: '%s' effect, %i sequencer, %i step):"
                                " step data is incorrect, step is skipped.\n"
                                % (effect, i_seq, i_step)
                        )
                        sequencer["Sequence"].remove(step)
                        continue

                    # check if step keys are correct (no wrong steps, brightness or repeat or wait in step)
                    error, w, wrong_keys, = Checker.check_step_keys(step)
                    if error:
                        warning += (
                                "Error: '%s' effect, %i sequencer, %i step): %s "
                                "This step is not loaded.\n"
                                % (effect, i_seq, i_step, error)
                        )
                        sequencer["Sequence"].remove(step)
                        continue
                    if wrong_keys:
                        warning += (
                                "Error: '%s' effect, %i sequencer, %i step): "
                                "%s this data is not loaded.\n" % (effect, i_seq, i_step, w)
                        )
                    for key in wrong_keys:
                        step.pop(key)

                    if "Name" in step.keys():
                        if not isinstance(step["Name"], str):
                            warning += (
                                    "Error: '%s' effect, %i sequencer, %i step): "
                                    "wrong name data, name is skipped.\n"
                                    % (effect, i_seq, i_step)
                            )
                            step.pop("Name")
                        else:
                            if step["Name"] in namelist:
                                warning += (
                                        "Error: '%s' effect, %i sequencer, %i step): "
                                        "name already used, name is skipped.\n"
                                        % (effect, i_seq, i_step)
                                )
                                step.pop("Name")
                            else:
                                namelist.append(step["Name"])

                    # check step brightness correct
                    error, brightness = Checker.check_brightness(step, leds_count)
                    if error:
                        warning += (
                                "Error: '%s' effect, %i sequencer, %i step: %s "
                                "step brightness is skipped.\n"
                                % (effect, i_seq, i_step, error)
                        )
                        if brightness:
                            step.pop(brightness)

                    # check wait parameters is correcr
                    error = Checker.check_wait(step)
                    if error:
                        warning += (
                                "Error: '%s' effect, %i sequencer, %i step: %s "
                                "step wait is skipped.\n" % (effect, i_seq, i_step, error)
                        )
                        step.pop("Wait")

                    # check if smooth parameter is correct
                    error, smooth = Checker.check_smooth(step)
                    if error:
                        warning += (
                                "Error: '%s' effect, %i sequencer, %i step: %s "
                                "step smooth is skipped.\n "
                                % (effect, i_seq, i_step, error)
                        )
                        step.pop(smooth)

                    # check repeat
                    error = Checker.check_repeat(step, namelist)
                    if error:
                        warning += (
                                "Error: '%s' effect, %i sequencer, %i step: %s. "
                                "This repeat step is not loaded\n "
                                % (effect, i_seq, i_step, error)
                        )
                        sequencer["Sequence"].remove(step)

        # remove effects with not list data
        for effect in wrong_effects:
            new_data.pop(effect)
        return new_data, None, warning
    # for everything unexpected
    except Exception:
        e = sys.exc_info()[1]
        return None, e.args[0], ""


def differences(a, b, section=None):
    for [c, d], [h, g] in zip(a.items(), b.items()):
        if not isinstance(d, dict) and not isinstance(g, dict):
            if d != g:
                yield (c, d, g, section)
        else:
            for i in differences(d, g, c):
                for b in i:
                    yield b


from pprint import pprint

#aux = DataLoad(led_raw_dict)
# print(aux.LedGroups[0])
# pprint(aux.Sequencers[0])

#pprint(dataclasses.asdict(aux))

# a, _, warnings = LoadDataFromText()
# print(list(differences(a, led_dict)))
# print(warnings)


class AuxEffect:

    def __init__(self):
        self.data = dict()
        self.sequencer_keys = ['config', 'sequence']


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
