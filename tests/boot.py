"""
Tests the boot sequence to emulate the GUI headless.
Used for testing features / debugging OmniSynth.

author: Omar Barazanji (omar@omniaura.co)
date: 10/23/21

company: Omni Aura LLC
"""

from ..omnisynth.src.omnisynth import omni
import os
current_dir = os.path.abspath("")
dsp_dir = current_dir.replace(
    "omnisynth-dev\\tests", "omnisynth-dsp\\").replace("\\", "/")

# import OmniSynth
os.chdir('../')

OmniSynth = omni.Omni()
# compiles all synthDefs.
OmniSynth.compile_patches(dsp_dir+"/patches")
# selects first patch.
OmniSynth.set_active_patch("tone1", dsp_dir)
OmniSynth.midi_learn_on = True  # turn on midi learn.

# Start Python OSC mainloop (this is an Event at 60 Hz in the GUI).
# while (True):
#     OmniSynth.open_stream()
