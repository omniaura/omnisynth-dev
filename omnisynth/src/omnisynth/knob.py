class Knob:
    def __init__(self, src, chan, initial_value=0, filter_name=''):
        self.src = src
        self.chan = chan
        self.filter_name = filter_name
        self.value = initial_value

    def set_value(self, value):
        self.value = value

    def set_filter_name(self, filter_name):
        self.filter_name = filter_name

    def __eq__(self, obj):
        return isinstance(obj, Knob) and obj.src == self.src and obj.chan == self.chan
