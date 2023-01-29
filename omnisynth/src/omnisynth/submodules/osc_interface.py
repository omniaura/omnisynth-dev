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
from pythonosc import dispatcher
from pythonosc import osc_server

# Used for sending via OSC
from pythonosc import udp_client

# used for sending bundles via OSC
from pythonosc import osc_bundle_builder
from pythonosc import osc_message_builder

# Used for Async Rx from SC
from pythonosc.osc_server import AsyncIOOSCUDPServer

import asyncio
import time
from .message_handler import MessageHandler
from .midi_handler import MidiHandler
from .knob_collection import KnobCollection
from .output_device_collection import OutputDeviceCollection
from .patch_collection import PatchCollection

from .patch import Patch

import redis
r = redis.Redis.from_url(url='redis://127.0.0.1:6379/0')

DELAY_MS = 50


class OscInterface:

    def __init__(self):
        self.midi_evnt = []
        self.midi_handler = MidiHandler()
        self.osc_command_dispatcher = dispatcher.Dispatcher()
        self.note_evnt_hist = dict()

        # our patches
        self.patches = PatchCollection()

        # knobs
        self.knobs = KnobCollection()

        # array holding our output devices
        self.output_devices = OutputDeviceCollection()

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
            (rx_args.ip, rx_args.port), self.osc_command_dispatcher, asyncio.get_event_loop())
        transport, protocol = await server.create_serve_endpoint()
        await self.loop()
        transport.close()

    def receive(self):
        asyncio.run(self.init_main())

    def handle_event(self, *args):
        command_name = args[0]
        command_args = []
        for arg in args:
            command_args.append(arg)
        self.message_handler.handle_message(command_name, command_args)

    def map_commands_to_dispatcher(self):
        self.message_handler = MessageHandler()
        self.message_handler.attach_message_listener(
            '/noteOn', self.handle_note_on)
        self.message_handler.attach_message_listener(
            '/noteOff', self.handle_note_off)
        self.message_handler.attach_message_listener(
            '/control', self.handle_control)
        self.message_handler.attach_message_listener(
            '/params', self.handle_params)
        self.message_handler.attach_message_listener(
            '/setOutputDevices', self.handle_set_output_devices)

    def handle_note_on(self, command_args):
        self.midi_handler.send_note(
            '/noteOn', command_args[0], command_args[1])

    def handle_note_off(self, command_args):
        self.midi_handler.send_note(
            '/noteOff', command_args[0], command_args[1])

    def handle_control(self, command_args):
        val = command_args[0]
        src = command_args[1]
        chan = command_args[2]

        if self.midi_learn_on:
            self.midi_learn(val, src, chan)

        knob = self.knobs.find_or_add_knob(src, chan)
        self.set_patch_param_value(knob.filter_name, param_name, value)

        return

    def set_patch_param_value(self, patch_filename, param_name, value):
        '''
        change a synth's param value.
            params:
                filter_name: select filter/param.
                value: filter/param value.
        '''
        self.patches.set_patch_param_value(
            patch_filename, param_name, param_value)

    def midi_learn(self, val, src, chan):
        self.knobs.set_knob_value(src, chan, val)

    def handle_params(self, command_args):
        """
        Processes a /params message
        """

        patch_filename = command_args[0]
        param_num = command_args[1]
        param_name = command_args[2]
        param_default_val = command_args[3]

        self.patches.set_patch_param_value(
            patch_filename, param_name, param_value)

    def handle_set_output_devices(self, command_args):
        self.output_devices.find_or_add_output_device(
            command_args[0], command_args[1])

    def map_knob_to_filter_name(self, src, chan, filter_name):
        self.knobs.set_knob_filter_name(src, chan, filter_name)


if __name__ == "__main__":
    sc = OscInterface()
