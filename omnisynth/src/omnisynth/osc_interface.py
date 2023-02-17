'''
Open Sound Control module for communicating with Supercollider.

author: Omar Barazanji (omar@omniaura.co)

Python 3.7.x

sources:
1) https://python-osc.readthedocs.io/en/latest/
2) https://docs.python.org/3.7/library/asyncio.html
'''

# used for receiving via OSC
import argparse
import json
from pythonosc import osc_server

# Used for sending via OSC
from pythonosc import udp_client
from pythonosc import dispatcher

# used for sending bundles via OSC
from pythonosc import osc_bundle_builder
from pythonosc import osc_message_builder

# Used for Async Rx from SC
from pythonosc.osc_server import AsyncIOOSCUDPServer

import asyncio
import time
from omnisynth.osc_message_sender import OscMessageSender
from omnisynth.teensy_midi_handler import TeensyMidiHandler
from omnisynth.knob_collection import KnobCollection
from omnisynth.output_device_collection import OutputDeviceCollection
from omnisynth.patch_collection import PatchCollection
from omnisynth.pattern_collection import PatternCollection

from omnisynth.patch import Patch

DELAY_MS = 50


class OscInterface:
    def __init__(self):
        self.midi_handler = TeensyMidiHandler()
        self.current_control_event = [None, None, None]

        # track running state of super collider server
        self.super_collider_booted = False

        # our patches
        self.patch_collection = PatchCollection()
        self.active_patch = None

        # knobs
        self.knob_collection = KnobCollection()

        # patterns
        self.pattern_collection = PatternCollection()
        self.active_pattern = None

        # array holding our output devices
        self.output_devices = OutputDeviceCollection()

        self.osc_dispatcher = dispatcher.Dispatcher()

        self.midi_learn_on = False

    async def loop(self):
        # sleep time
        await asyncio.sleep(DELAY_MS * 0.001)

    async def init_main(self):
        rx = argparse.ArgumentParser()
        rx.add_argument("--ip", default="127.0.0.1", help="osc default ip")
        rx.add_argument("--port", type=int, default=7771,
                        help="supercollider tx osc port")
        rx_args = rx.parse_args()
        server = osc_server.AsyncIOOSCUDPServer(
            (rx_args.ip, rx_args.port), self.osc_dispatcher, asyncio.get_event_loop())
        transport, protocol = await server.create_serve_endpoint()
        await self.loop()
        transport.close()

    def process_midi_event(self):
        asyncio.run(self.init_main())

    def set_active_patch(self, patch_filename):
        """
        Sets the patch with the given filename to the currently active patch. If the patch has not yet been added and compiled,
        it will be before being set active.

        Args:
            patch_filename (String): the filename of the patch to set active
        """
        print(f'Setting active patch to {patch_filename}')
        self.active_patch = self.patch_collection.find_or_add_patch(
            patch_filename)

        OscMessageSender.send_omni_message(
            "selectPatch", patch_filename)

    def set_active_pattern(self, pattern_filename):
        """
        Sets the pattern with the given filename to the currently active pattern. If the pattern has not yet been added and compiled,
        it will be before being set active.

        Args:
            pattern_filename (String): the filename of the pattern to set active
        """
        print(f'Setting active pattern to {pattern_filename}')
        self.active_pattern = self.pattern_collection.find_or_add_pattern(
            pattern_filename)

        OscMessageSender.send_omni_message(
            "selectPattern", pattern_filename)

    def map_commands_to_dispatcher(self):
        self.osc_dispatcher.map('/noteOn', self.handle_note_on)
        self.osc_dispatcher.map('/noteOff', self.handle_note_off)
        self.osc_dispatcher.map('/control', self.handle_control)
        self.osc_dispatcher.map(
            '/initPatchParams', self.handle_init_patch_params)
        self.osc_dispatcher.map('/setOutputDevices',
                                self.handle_set_output_devices)
        self.osc_dispatcher.map('/superColliderStatus',
                                self.handle_super_collider_status)

    def handle_note_on(self, *command_args):
        pass
        # self.midi_handler.send_note(
        #     '/noteOn', command_args[1], command_args[2])

    def handle_note_off(self, *command_args):
        pass
        # self.midi_handler.send_note(
        #     '/noteOff', command_args[1], command_args[2])

    def handle_control(self, *command_args):
        val = command_args[1]
        src = command_args[2]
        chan = command_args[3]

        self.current_control_event = [val, src, chan]

        knob = self.knob_collection.find_or_add_knob(src, chan)

        if self.midi_learn_on:
            knob.set_value(val, src, chan)

        if knob.filter_name != '':
            self.active_patch.sync_param(
                knob.filter_name, val)

    def handle_init_patch_params(self, *command_args):
        """
        Processes a /initPatchParams message
        """
        patch_name = command_args[1]
        param_num = command_args[2]
        param_name = command_args[3]
        param_default_val = command_args[4]

        patch = self.patch_collection.find_patch_by_name(patch_name)
        patch.set_param_initial_value(param_name, param_default_val)

    def handle_set_output_devices(self, *command_args):
        """
        Processes a /setOutputDevices message
        Message: [[device_index1, device_name1], ...]

        Args:
            command_args (array): the command arguments
        """
        for i in range(1, len(command_args)):
            device = command_args[i].split(b',')
            self.output_devices.find_or_add_output_device(
                int.from_bytes(device[0], 'big'), device[1].decode()[1:]
            )

        print('Done setting output devices')

    def handle_super_collider_status(self, *command_args):
        print(command_args)
        if command_args[1] == 'running':
            print(f'Setting supercollider server status to running...')
            self.super_collider_booted = True


if __name__ == "__main__":
    sc = OscInterface()
