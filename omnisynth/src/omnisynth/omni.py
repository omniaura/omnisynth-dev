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
        self.numPatch = 0
        self.patchIndex = 0  # indexes for quick select on main screen
        self.patchListIndex = dict()
        self.patternListIndex = dict()

        # all possible synth params.
        self.param_table = [
            "attack", "decay", "sustain", "release",
            "lpf", "hpf", "mod_freq", "lin_start",
            "lin_stop", "lin_duration"
        ]

    # opens UDP stream for MIDI control messages.
    def open_midi_control_msg_stream(self, *args):
        self.osc_interface.receive()
        try:
            # grab first index (tag) if it exists
            event = self.osc_interface.midi_evnt[0]
        except IndexError:
            event = ""

        if event != "/control":
            return

        # save entire message
        self.control_evnt = self.osc_interface.midi_evnt
        if self.midi_learn_on:
            self.midi_learn(self.control_evnt)

        try:
            self.knob_map = ast.literal_eval(r.get('mapKnob').decode())
            knob_table = json.loads(r.get('knobTable'))
        except:
            self.knob_map = dict()

        if len(self.knob_map) != 0:
            for knob_addr in self.knob_map:
                filter_name = self.knob_map[knob_addr]
                try:
                    raw_value = knob_table[str(
                        knob_addr[0])][str(knob_addr[1])]['val']
                except:
                    break
                self.filter_sel(filter_name, raw_value)
        self.osc_interface.midi_evnt = []

    def compile_patches(self, folder, parentDir=''):
        if len(parentDir) != 0:
            directory = parentDir + "%s/" % folder
        else:
            directory = "%s/" % folder

        command = "/omni"
        control = "compile"
        for patch in os.listdir(directory):
            filedir = directory + patch
            path = os.path.abspath(filedir).replace("\\", "/")
            OscMessageSender.send_message(command, control, path)
        return self.osc_interface.patch_param_table

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
            OscMessageSender.send_message(command, control, path)
        return self.osc_interface.patch_param_table

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
            command = "/omni"
            control = "controlPattern"
            OscMessageSender.send_message(command, "compile", path)
            OscMessageSender.send_message(
                command, control, action, path)
        else:  # start / stop
            command = f"/{pattern_name}"
            control = "playerSel"
            OscMessageSender.send_message(command, control, action)

        self.pattern = pattern_name
        r.set("pattern", self.pattern)

    def stop_sc_synth(self):
        command = "/omni"
        control = "stopScSynth"
        OscMessageSender.send_message(command, control)

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
        if len(midi_msg) == 4:
            val = midi_msg[1]
            src = midi_msg[2]
            chan = midi_msg[3]
            knob_arr = {chan: {'val': val}}
            if src in self.knob_table.keys():
                if chan in self.knob_table[src].keys():
                    self.knob_table[src][chan]['val'] = val
                else:
                    self.knob_table[src][chan] = {'val': val}
            else:
                self.knob_table[src] = knob_arr
            r.set('knobTable', json.dumps(self.knob_table))

    def map_knob(self, src, chan, filter_name):
        self.osc_interface.map_knob_to_filter_name(src, chan, filter_name)

# Quickly maps a table of param names to all knobs needed.


def quick_map(OmniSynth):
    itr = 0
    for key, value in OmniSynth.knob_table.items():
        OmniSynth.map_knob(key, OmniSynth.param_table[itr])
        itr += 1
        if itr == len(OmniSynth.param_table):
            break


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
