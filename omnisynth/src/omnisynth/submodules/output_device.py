class OutputDevice:
    def __init__(self, index, name):
        self.index = index
        self.name = name

    def __eq__(self, obj):
        return isinstance(obj, OutputDevice) and obj.index == self.index and obj.name == self.name
