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

import redis
r = redis.Redis.from_url(url='redis://127.0.0.1:6379/0')

DELAY_MS = 50

OSC_COMMANDS = [
    '/noteOff',
    '/noteOn',
    '/control'
    '/params'
    '/outDev'
    '/server'
]


class OscInterface:

    def __init__(self):
        self.midi_evnt = []
        OmniMidi.open_midi_connection()
        self.osc_command_dispatcher = dispatcher.Dispatcher()
        self.note_evnt_hist = dict()

        # dictionary holding all patches and their parameters.
        #     organization: self.patch_param_table[(synth, param_num)] = [param_name, default_val]]
        self.patch_param_table = dict()

        # array holding our patches
        self.patches = []
        r.delete('patchTable')

        # dictionary holding all output devices and their index in SC.
        #     organization: self.out_dev_table[dev_num] = out_dev_name
        self.out_dev_table = dict()

        # array holding our output devices
        # todo: make OutputDevice a python object
        self.output_devices = []

    def handle_event(self, *args):
        command_name = args[0]
        command_args = []
        for arg in args:
            command_args.append(arg)
        MessageHandler(command_name, command_args).handle_message()

    def rx_handler(self, *args):
        event = []
        for x in args:
            event.append(x)
        self.midi_evnt = event
        if event[0] == "/noteOn" or event[0] == "/noteOff":
            self.teensy.send_note(event)
        if event[0] == "/params":
            param = event
            synth = param[1]
            param_num = param[2]
            param_name = param[3]
            param_default_val = param[4]

            param_arr = {'params': {param_name: param_default_val}}
            key = synth
            if key in self.patch_param_table:
                if not str(param_arr['params']) in str(self.patch_param_table[key]['params']):
                    self.patch_param_table[key]['params'][param_name] = param_default_val
                    r.set('patchTable', json.dumps(self.patch_param_table))
            else:
                self.patch_param_table[key] = param_arr
                r.set('patchTable', json.dumps(self.patch_param_table))

        if event[0] == "/outDev":
            dev_num = event[1]
            dev_name = event[2]
            if dev_num not in self.out_dev_table:
                self.out_dev_table[dev_num] = dev_name
            r.set('outDevTable', json.dumps(self.out_dev_table))

        if event[0] == "/server":
            value = event[1]
            r.set("serverStatus", value)

        print(event)

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

    def map_commands_to_dispatcher(self):
        for command_name in OSC_COMMANDS:
            self.osc_command_dispatcher.map(command_name, self.handle_event)

    def map_dispatcher(self, sc_variable):
        self.osc_command_dispatcher.map(sc_variable, self.rx_handler)

    def transmit(self, command, control, *args):
        port = 57120
        if (command == "server"):
            port = 57110
        tx = argparse.ArgumentParser()
        tx.add_argument("--ip", default="127.0.0.1", help="osc default ip")
        tx.add_argument("--port", type=int, default=port,
                        help="supercollider rx osc port")
        tx_args = tx.parse_args()
        client = udp_client.SimpleUDPClient(tx_args.ip, tx_args.port)

        if command == "server":
            client.send_message(control, args[0])
        else:
            control_block = [control]
            for x in args:
                control_block.append(x)
            message = (command, control_block)
            client.send_message(command, control_block)


if __name__ == "__main__":
    sc = OmniCollider()
