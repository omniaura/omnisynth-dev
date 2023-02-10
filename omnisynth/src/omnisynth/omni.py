"""
Main / Top Level for the OmniAura Synthesizer.

author: Omar Barazanji (omar@omniaura.co)

Python 3.7.x
"""

from submodules.osc_message_sender import OscMessageSender
from submodules.osc_interface import OscInterface
from submodules.patch import Patch
from submodules.value_converter import ValueConverter

import platform
import redis
import json
import numpy as np
import os
import ast
import psutil

r = redis.Redis.from_url(url='redis://127.0.0.1:6379/0')

OS = 'Windows'
if platform.system() == 'Linux':
    OS = 'Linux'
elif platform.system() == 'Darwin':
    OS = 'Darwin'

if 'Darwin' in OS or 'Linux' in OS:  # Mac or Linux
    OMNISYNTH_PATH = os.getcwd().replace(
        'omnisynth-dev/omnisynth/src/omnisynth', 'omnisynth-dsp/')
else:  # Windows
    OMNISYNTH_PATH = os.getcwd().replace(
        'omnisynth-dev\\omnisynth\\src\\omnisynth', 'omnisynth-dsp/').replace("\\", "/")

# Used for sending / receiving data from supercollider.
# when import omnisynth is called (for production)
# # when running locally before building wheel (for testing)
# from .omnimidi import OmniMidi
# from .osc_interface import OscInterface
# from .osc_message_sender import OscMessageSender


class Omni():

    def __init__(self):
        # initialize OSC module for UDP communication with Supercollider.
        self.osc_interface = OscInterface()
        self.osc_interface.map_commands_to_dispatcher()

        # current song selected.
        self.song = "song1"
        r.set('song', self.song)

        # current pattern selected.
        self.pattern = "pattern1"
        r.set("pattern", self.pattern)

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
            self.osc_interface.patch_collection.find_or_add_patch(
                patch_filename)

        # Return the patches we have compiled
        return self.osc_interface.patch_collection

    def start_pattern(self, pattern_name):
        self.osc_interface.pattern_collection.find_or_add_pattern(
            pattern_name).start()

    def stop_pattern(self, pattern_name):
        self.osc_interface.pattern_collection.find_or_add_pattern(
            pattern_name).stop()

    def start_sc_process(self):
        sc_main = OMNISYNTH_PATH + "main.scd"

        if OS == 'Windows':
            subprocess.Popen(["sclang", sc_main])
        else:
            subprocess.Popen(
                ["/Applications/SuperCollider.app/Contents/MacOS/sclang", sc_main])

    def stop_sc_processes(self):
        """
        Stops the ScSynth and sclang processes
        """
        OscMessageSender.send_omni_message('stopScSynth')
        sc_lang_process_name = "sclang.exe"
        sc_synth_process_name = "scsynth.exe"
        process_names = [
            "sclang.exe",
            "scsynth.exe"
        ]
        for proc in psutil.process_iter():
            if proc.name() in process_names:
                proc.kill()

    def sc_server_booted(self):
        """
        The status of the SuperCollider server

        Returns:
            str: 'Running' if the server is running, 'Stopped' if the server is stopped
        """
        return self.osc_interface.super_collider_booted

    def set_active_patch_param_value(self, param_name, value):
        """
        Change a parameter value for the currently active patch

        Args:
            param_name (String): the name of the parameter
            value (number): the value of the parameter
        """
        real_value = ValueConverter.converted_value(param_name, value)
        self.osc_interface.active_patch.sync_param(
            param_name, real_value)

    def set_active_pattern_param_value(self, param_name, value):
        '''
        change a patterns's param value.
            params:
                param_name: select param.
                value: filter/param value.
                pattern_name (optional): change a specific pattern's parameter.
        '''
        self.osc_interface.active_pattern.sync_param(param_name, value)

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

        self.osc_interface.knob_collection.set_knob_value(val, src, chan)

    def map_knob(self, src, chan, param_name):
        """
        Map a knob to a patch parameter name

        Args:
            src (number): the knob src
            chan (number): the knob channel
            param_name (str): the patch parameter name to map this knob to
        """
        self.osc_interface.knob_collection.set_knob_filter_name(
            src, chan, param_name)

    # opens UDP stream for MIDI control messages.
    def open_stream(self, *args):
        self.osc_interface.process_midi_event()

    def set_midi_learn(self, on):
        self.osc_interface.midi_learn_on = on

    def current_control_event(self):
        self.osc_interface.current_control_event


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

    OmniSynth = Omni()
    OmniSynth.set_midi_learn(True)  # turn on midi learn.

    def sc_thread():
        OmniSynth.start_sc_process()

    def omni_thread():
        compiled = False
        while (True):
            OmniSynth.open_stream()
            if OmniSynth.sc_server_booted():
                if not compiled:
                    # compiles all synthDefs.
                    OmniSynth.compile_patches(
                        OMNISYNTH_PATH+"patches")
                    OmniSynth.set_active_patch(
                        OMNISYNTH_PATH + "patches/tone1.scd")
                    compiled = True

    omnithread = Thread(target=omni_thread)
    omnithread.start()

    scthread = Thread(target=sc_thread)
    scthread.start()
    scthread.join()
