'''
Single omni instance for the server to use and handle state (service).
'''

import redis
from omnisynth import omni
from constants import OMNISYNTH_PATH

OMNISYNTH_PATH = OMNISYNTH_PATH.replace("/modules", "")


class OmniInstance:

    def __init__(self):
        self.OmniSynth = omni.Omni()

    def compile_patches(self):
        self.OmniSynth.compile_patches(OMNISYNTH_PATH+"patches")

    def open(self):
        self.OmniSynth.midi_learn_on = True
        self.OmniSynth.open_stream()


if __name__ == "__main__":
    oi = OmniInstance()
    while True:
        oi.open()
