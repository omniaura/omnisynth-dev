from .knob import Knob


class KnobCollection:
    def __init__(self):
        self.knobs = []

    def set_knob_value(self, src, chan, value):
        # set knob value given its src and channel
        # if the knob currently doesnt exist within our knob collection, add it
        knob = self.find_or_add_knob(src, chan)
        knob.set_value(value)

    def set_knob_filter_name(self, src, chan, filter_name):
        # set knob filter name given its src and channel
        # if the knob currently doesn't exist, add it
        knob = self.find_or_add_knob(src, chan)
        knob.set_filter_name(filter_name)

    def find_or_add_knob(self, src, chan):
        for knob in self.knobs:
            if knob.src == src and knob.chan == chan:
                return knob

        knob = Knob(src, chan)
        self.knobs.append(knob)
        return knob
