"""
Main / Top Level for the OmniAura Synthesizer.

author: Omar Barazanji (omar@omniaura.co)

Python 3.7.x
"""

import platform
import redis
import json
import numpy as np
import os
import ast

r = redis.Redis.from_url(url='redis://127.0.0.1:6379/0')

OS = 'Windows'
if platform.system() == 'Linux':
    OS = 'Linux'
elif platform.system() == 'Darwin':
    OS = 'Darwin'

# Used for sending / receiving data from supercollider.
try:
    # when import omnisynth is called (for production)
    from .submodules.omnimidi import OmniMidi
    from .submodules.osc_interface import OscInterface
    from .submodules.osc_message_sender import OscMessageSender
except:
    # when running locally before building wheel (for testing)
    from submodules.omnimidi import OmniMidi
    from submodules.osc_interface import OscInterface
    from submodules.osc_message_sender import OscMessageSender


class Omni():

    def __init__(self):

        # initialize OSC module for UDP communication with Supercollider.
        self.osc_interface = OscInterface()
        self.osc_interface.map_commands_to_dispatcher()

        # current synth selected.
        self.synth = "tone1"
        r.set('synth', self.synth)

        # current song selected.
        self.song = "song1"
        r.set('song', self.song)

        # current pattern selected.
        self.pattern = "pattern1"
        r.set("pattern", self.pattern)

        # holds control events from UDP stream.
        self.control_evnt = []

        # holds note on / off events from UDP stream.
        self.note_evnt = []

        # used for turning on midi learn.
        self.midi_learn_on = False

        # holds all control knobs and their values.
        #     organization: self.knob_table[knob_addr] = value
        #     where knob_addr = (src, chan) from the MIDI cc knob.
        self.knob_table = dict()
        r.delete('knobTable')

        # holds all knob mappings to SC params.
        #     organization: self.knob_map[knob_addr] = filter_name.
        self.knob_map = dict()
        r.delete('mapKnob')

        # holds history of last value sent through the UDP stream to SC.
        #     organization: self.knob_map_hist[filter_name] = value.
        self.knob_map_hist = dict()

        self.note_evnt_hist = dict()

        # Table that will be outputted to DAC & Mux.
        self.cv_table = [[0 for x in range(8)] for y in range(4)]

        # Variables For GUI.
        self.mapMode = False

        # all possible synth params.
        self.param_table = [
            "attack", "decay", "sustain", "release",
            "lpf", "hpf", "mod_freq", "lin_start",
            "lin_stop", "lin_duration"
        ]

    def compile_patches(self, folder, parentDir=''):
        if len(parentDir) != 0:
            directory = parentDir + "%s/" % folder
        else:
            directory = "%s/" % folder

        # Add all patches via filenames through our osc_interface#add_patch method
        for patch in os.listdir(directory):
            filedir = directory + patch
            patch_filename = os.path.abspath(filedir).replace("\\", "/")
            self.osc_interface.add_patch(patch_filename)

        # Return the patches we have compiled
        return self.osc_interface.patches

    # saves state of which song is currently selected.
    def song_sel(self, song_name):
        self.song = song_name

    # toggles and controls patterns created in supercollider
    def pattern_sel(self, pattern_name, action, *args):
        if not len(args) == 0:
            parentDir = args[0]
            directory = parentDir + \
                "patterns/songs/%s/%s.scd" % (self.song, pattern_name)
        else:
            directory = "patterns/songs/%s/%s.scd" % (self.song, pattern_name)
        path = os.path.abspath(directory).replace("\\", "/")
        if action == 'compile':
            OscMessageSender.send_omni_message("compile", path)
            OscMessageSender.send_omni_message("controlPattern", action, path)
        else:  # start / stop
            OscMessageSender.send_message(
                f"/{pattern_name}", "playerSel", action)

        self.pattern = pattern_name
        r.set("pattern", self.pattern)

    def stop_sc_synth(self):
        OscMessageSender.send_omni_message('stopScSynth')

    def filter_sel(self, filter_name, value):
        '''
        change a synth's param value.
            params:
                filter_name: select filter/param.
                value: filter/param value.
        '''
        synth = r.get('synth').decode()
        command = "/%s" % synth
        control = "setParam"
        real_value = self.value_map(filter_name, value)
        if filter_name in self.knob_map_hist and self.knob_map_hist[filter_name] != value:
            OscMessageSender.send_message(
                command, control, filter_name, real_value)
            self.knob_map_hist[filter_name] = value
        elif filter_name not in self.knob_map_hist:  # if first instance
            OscMessageSender.send_message(
                command, control, filter_name, real_value)
            self.knob_map_hist[filter_name] = value

    def pattern_param_sel(self, param_name, value):
        '''
        change a patterns's param value.
            params:
                param_name: select param.
                value: filter/param value.
                pattern_name (optional): change a specific pattern's parameter.
        '''
        pattern_name = r.get("pattern").decode()
        command = "/%s" % pattern_name
        control = "setParam"
        parameter = param_name
        print('sending:')
        print(command, control, parameter, value)
        OscMessageSender.send_message(
            command, control, parameter, value)

    # creates dict for all control knobs on MIDI controller.

    def midi_learn(self, midi_msg):
        if len(midi_msg) != 4:
            return

        val = midi_msg[1]
        src = midi_msg[2]
        chan = midi_msg[3]

        self.osc_interface.set_knob_value(val, src, chan)

    def map_knob(self, src, chan, filter_name):
        self.osc_interface.map_knob_to_filter_name(src, chan, filter_name)


"""
Main entrypoint
Initializes main Omni process and listeners
"""
if __name__ == "__main__":
    '''
    For testing run `python -i omni.py` to get access to all OmniSynth functions while SC runs.
    '''
    import subprocess
    from threading import Thread
    # get omnisynth-dsp path
    if 'Darwin' in OS or 'Linux' in OS:  # Mac or Linux
        OMNISYNTH_PATH = os.getcwd().replace(
            'omnisynth-dev/omnisynth/src/omnisynth', 'omnisynth-dsp/')
    else:  # Windows
        OMNISYNTH_PATH = os.getcwd().replace(
            'omnisynth-dev\\omnisynth\\src\\omnisynth', 'omnisynth-dsp/').replace("\\", "/")

    OmniSynth = Omni()
    OmniSynth.sc_compile(OMNISYNTH_PATH+"/patches")  # compiles all synthDefs.
    # selects first patch.
    OmniSynth.select_patch(patch_filename)("tone1", OMNISYNTH_PATH)
    OmniSynth.midi_learn_on = True  # turn on midi learn.
    sc_main = OMNISYNTH_PATH + "main.scd"

    def sc_thread():
        if 'Darwin' in OS:
            subprocess.Popen(
                ["/Applications/SuperCollider.app/Contents/MacOS/sclang", sc_main])
        else:
            subprocess.Popen(["sclang", sc_main])

    def omni_thread():
        while (True):
            OmniSynth.open_stream()

    omnithread = Thread(target=omni_thread)
    omnithread.start()
    scthread = Thread(target=sc_thread)
    scthread.start()
    scthread.join()
