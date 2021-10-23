"""
Main / Top Level for the OmniAura Synthesizer.

author: Omar Barazanji
date: 11/12/20

Python 3.7.x
"""

import numpy as np
import os


# Used for sending / receiving data from supercollider.
from .submodules.omnimidi import OmniMidi
from .submodules.osc import OmniCollider

class Omni():

    def __init__(self):

        # initialize OSC module for UDP communication with Supercollider.
        self.sc = OmniCollider(17)
        self.sc.map_dispatcher("/control")
        self.sc.map_dispatcher("/noteOn")
        self.sc.map_dispatcher("/noteOff")
        self.sc.map_dispatcher("/params")
        self.sc.map_dispatcher("/outDev")

        # current synth selected.
        self.synth = "tone1"

        # current song selected.
        self.song = "song1"

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

        # holds all knob mappings to SC params.
        #     organization: self.knob_map[knob_addr] = filter_name.
        self.knob_map = dict()

        # holds history of last value sent through the UDP stream to SC.
        #     organization: self.knob_map_hist[filter_name] = value.
        self.knob_map_hist = dict()

        self.note_evnt_hist = dict()

        # Table that will be outputted to DAC & Mux.
        self.cv_table = [[0 for x in range(8)] for y in range(4)] 

        # LUT for freq control messages, maps 0-127 to 20 - 20000 Hz.
        self.cc_to_freq = np.linspace(20,20000,128).tolist()

        # LUT for adsr control messages, maps 0-127 to .001 - 1 (seconds or amplitude).
        self.cc_to_adsr = np.linspace(0.001, 2, 128).tolist()

        # LUT for linear envelope params.
        self.cc_to_lin = np.linspace(1,3000, 128).tolist()

        # LUT for duration.
        self.cc_to_duration = np.linspace(0.001, 5, 128).tolist()

        # Variables For GUI.
        self.mapMode = False
        self.numPatch = 0
        self.patchIndex = 0 #indexes for quick select on main screen
        self.patchListIndex = dict()
        self.patternListIndex = dict()

        # all possible synth params.
        self.param_table = [
            "attack", "decay", "sustain", "release",
            "lpf", "hpf", "mod_freq", "lin_start",
            "lin_stop", "lin_duration"
        ]

    def value_map(self, filt, inp):
        value = inp
        if filt == "lpf" or filt == "hpf":
            value = self.cc_to_freq[int(inp)]
        if filt == "attack" or filt == "decay" or filt == "sustain" or filt == "release":
            value = self.cc_to_adsr[int(inp)]
        if filt == "lin_start" or filt == "lin_stop":
            value = self.cc_to_lin[int(inp)]
        if filt == "lin_duration":
            value = self.cc_to_duration[int(inp)]
        return value

    # opens UDP stream for MIDI control messages.
    def open_stream(self, *args):
        self.sc.receive()
        try:
            # grab first index (tag) if it exists
            event = self.sc.midi_evnt[0]
        except IndexError:
            event = ""

        if event == "/control":
            # save entire message
            self.control_evnt = self.sc.midi_evnt
            if self.midi_learn_on:
                self.midi_learn(self.control_evnt)
            if len(self.knob_map) != 0:
                for knob_addr in self.knob_map:
                    filter_name = self.knob_map[knob_addr]
                    raw_value = self.knob_table[knob_addr]
                    self.filter_sel(filter_name, raw_value)
            self.sc.midi_evnt = []  

    # compiles all synthDef's in dsp folder.
    def sc_compile(self, typeDef, *args):

        if not len(args) == 0: 
            parentDir = args[0]
            directory = parentDir + "%s/" % typeDef
        else:
            directory = "%s/" % typeDef
        command = "/omni"
        control = "compile"
        for patch in os.listdir(directory):
            filedir = directory + patch
            path = os.path.abspath(filedir).replace("\\", "/")
            self.sc.transmit(command, control, path)

    # saves state of which song is currently selected.
    def song_sel(self, song_name):
        self.song = song_name

    # toggles and controls patterns created in supercollider
    def pattern_sel(self, pattern_name, action, *args):
        if not len(args) == 0: 
            parentDir = args[0]
            directory = parentDir + "patterns/songs/%s/%s.scd" % (self.song, pattern_name)
        else:
            directory = "patterns/songs/%s/%s.scd" % (self.song, pattern_name)
        command = "/omni"
        control = "pdef_control"
        path = os.path.abspath(directory).replace("\\", "/")
        self.sc.transmit(command, "compile", path)
        self.sc.transmit(command, control, action, path, pattern_name)

    # turns on / off synthDef's from SC.
    def synth_sel(self, synth_name, *args):
        if not len(args) == 0: 
            parentDir = args[0]
            directory = parentDir + "patches/%s.scd" % synth_name
        else:
            directory = "patches/%s.scd" % synth_name
        command = "/omni"
        control = "synthSel"
        self.synth = synth_name
        synth_path = os.path.abspath(directory).replace("\\", "/")
        self.sc.transmit(command, control, synth_name, synth_path)

    def exit_sel(self):
        command = "/omni"
        control = "exitSel"
        self.sc.transmit(command, control)

    def out_dev_sel(self,dev_num):
        command = "/omni"
        control = "outDevSel"
        dev_name = self.sc.out_dev_table[dev_num]
        self.sc.transmit(command, control, dev_name)

    # select filter and param value.
    def filter_sel(self, filter_name, value):
        command = "/%s" % self.synth
        control = "filterSel"
        real_value = self.value_map(filter_name,value)
        if filter_name in self.knob_map_hist and self.knob_map_hist[filter_name] != value:
            self.sc.transmit(command, control, filter_name, real_value)
            self.knob_map_hist[filter_name] = value
        elif filter_name not in self.knob_map_hist: # if first instance
            self.sc.transmit(command, control, filter_name, real_value)
            self.knob_map_hist[filter_name] = value

    # creates dict for all control knobs on MIDI controller.
    def midi_learn(self, midi_msg):
        if len(midi_msg) == 4:
            val = midi_msg[1]
            src = midi_msg[2]
            chan = midi_msg[3]
            self.knob_table[(src,chan)] = val

    # maps a knob to an SC parameter.
    # params:
    #     knob_addr = (src, chan) 
    #     filter_name = "lpf" (for example)
    def map_knob(self, knob_addr, filter_name):
        self.knob_map[knob_addr] = filter_name

# Quickly maps a table of param names to all knobs needed.
def quick_map(OmniSynth):
    itr=0
    for key, value in OmniSynth.knob_table.items():
        OmniSynth.map_knob(key, OmniSynth.param_table[itr])
        itr += 1
        if itr==len(OmniSynth.param_table): break



