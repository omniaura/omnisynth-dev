'''
Boots the OmniSynth Server for API calls and starts an instance of SuperCollider (OmniSynth DSP)
'''

import subprocess

# import OmniSynth
from omnisynth import omni
from modules.constants import OMNISYNTH_PATH

# start supercollider server and simulates the GUI's event loop as `While True`.
def start_sc(event_loop=True):
    sc_main = OMNISYNTH_PATH + "main.scd"
    subprocess.Popen(["sclang", sc_main])
    # initialize OmniSynth instance
    OmniSynth = omni.Omni()
    OmniSynth.sc_compile(OMNISYNTH_PATH+"patches") # compiles all synthDefs.
    OmniSynth.synth_sel("tone1", OMNISYNTH_PATH) # selects first patch.
    OmniSynth.midi_learn_on = True # turn on midi learn.

    def open_loop():
        # Start Python OSC mainloop (this is an Event at 60 Hz in the GUI).
        while (True):
            OmniSynth.open_stream() # used to grab knob values and update GUI in realtime (stream)

    if event_loop: open_loop()

# starts the server as a subprocess
def start_server():
    subprocess.Popen(['python', 'modules/start_server.py'])


if __name__ == "__main__":
    start_server()
    # start_sc(False)