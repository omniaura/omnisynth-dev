"""
Tests the boot sequence to emulate the GUI headless.
Used for testing features / debugging OmniSynth.

author: Omar Barazanji (omar@omniaura.co)
date: 10/23/21

company: Omni Aura LLC
"""

import os
current_dir = os.path.abspath("")
dsp_dir = current_dir.replace("omnisynth-dev\\tests", "omnisynth-dsp\\").replace("\\","/")

# import OmniSynth
os.chdir('../')
from ..omnisynth.src.omnisynth import omni

OmniSynth = omni.Omni()
OmniSynth.sc_compile(dsp_dir+"/patches") # compiles all synthDefs.
OmniSynth.synth_sel("tone1", dsp_dir) # selects first patch.
OmniSynth.midi_learn_on = True # turn on midi learn.

# Start Python OSC mainloop (this is an Event at 60 Hz in the GUI).
while (True):
    OmniSynth.open_stream()