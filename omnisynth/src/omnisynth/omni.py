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
    from .omnimidi import OmniMidi
    from .osc_interface import OscInterface
    from .osc_message_sender import OscMessageSender


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

        # used for turning on midi learn.
        self.midi_learn_on = False

        # Variables For GUI.
        self.mapMode = False

    def compile_patches(self, folder, parentDir=''):
        """
        Compile patches within a directory

        Args:
            folder (str): the folder that contains the patch files
            parentDir (str, optional): the parent directory of the folder. defaults to ''

        Returns:
            PatchCollection: the collection of compiled patches
        """
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
    # TODO: refactor me
    def song_sel(self, song_name):
        self.song = song_name

    # toggles and controls patterns created in supercollider
    # TODO: refactor me
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
            OscMessageSender.send_client_message(
                f"/{pattern_name}", "playerSel", action)

        self.pattern = pattern_name
        r.set("pattern", self.pattern)

    def stop_sc_synth(self):
        """
        Stops the ScSynth process
        """
        OscMessageSender.send_omni_message('stopScSynth')

    def sc_server_boot_status(self):
        """
        The status of the SuperCollider server

        Returns:
            str: 'Running' if the server is running, 'Stopped' if the server is stopped
        """
        if self.osc_interface.super_collider_booted:
            return 'Running'

        return 'Stopped'

    def set_patch_parameter_value(self, param_name, value):
        """
        Change a parameter value for the currently active patch

        Args:
            param_name (String): _description_
            value (number): _description_
        """
        self.osc_interface.set_patch_param_value(
            self.osc_interface.active_patch().filename, param_name, value)

    # TODO: refactor me
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

    def active_patch(self):
        """
        Retrieves the currently active Patch

        Returns:
            Patch: the currently active patch
        """
        return self.osc_interface.patch_collection.active_patch

    def set_active_patch(self, patch_filename):
        """
        Sets the currently active patch. Compiles the patch if not already compiled

        Args:
            patch_filename (str): the filename of the patch
        """
        self.osc_interface.patch_collection.set_active_patch(patch_filename)

    def midi_learn(self, midi_msg):
        """
        Set a knob value from a MIDI message

        Args:
            midi_msg (list): the midi message
        """
        if len(midi_msg) != 4:
            return

        val = midi_msg[1]
        src = midi_msg[2]
        chan = midi_msg[3]

        self.osc_interface.set_knob_value(val, src, chan)

    def map_knob(self, src, chan, param_name):
        """
        Map a knob to a patch parameter name

        Args:
            src (number): the knob src
            chan (number): the knob channel
            param_name (str): the patch parameter name to map this knob to
        """
        self.osc_interface.map_knob_to_filter_name(src, chan, param_name)

    # opens UDP stream for MIDI control messages.
    def open_stream(self, *args):
        self.osc_interface.process_midi_event()


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
