'''
Single omni instance for the server to use and handle state (service).
'''

from omnisynth import omni
from constants import OMNISYNTH_PATH

OMNISYNTH_PATH = OMNISYNTH_PATH.replace("/modules","")    


import redis

# moved to inside osc handler in omnisynth
# r = redis.Redis.from_url(url='redis://127.0.0.1:6379/0')

class OmniInstance:

    def __init__(self):
        self.OmniSynth = omni.Omni()

    def compile_patches(self):
        self.OmniSynth.sc_compile(OMNISYNTH_PATH+"patches")
        # r.set('patchTable', str(table))

    def open(self):
        self.OmniSynth.open_stream()


if __name__ == "__main__":
    oi = OmniInstance()
    while True:
        oi.open()