import json


class AuxEffects:

    def __init__(self):
        self.data = dict()


    def AddEffect(self, name: str):
        self.data[name] = list()

    def GetEffectsList(self):
        return self.data.keys()


    def GetUsedLedsList(self, effect: str):
        ledsused = list()
        try:
            sequencers = self.data[effect]
        except KeyError:
            print("No such effect % s" % effect)#ToDo add logging
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
            print("No such effect % s" % effect)  #ToDo add logging
        sequencers.append({"Config": leds, "Sequence": []})
        print(self.data)


    def CreateStep(self, effect:str, number:int, name: str, brightnesses:list, wait: int, smooth: int):
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
            print("Cannot add step to %i sequencer of %s effect" % (number, effect)) #ToDo add Logging
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
            print("Cannot add step to %i sequencer of %s effect" % (number, effect)) #ToDo add Logging
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


    def GetRepeatList(self, effect: str, number:int):
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

