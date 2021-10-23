'''
Open Sound Control module for communicating with Supercollider.

author: Omar Barazanji
date: 1/17/2021

Python 3.7.x

sources:
1) https://python-osc.readthedocs.io/en/latest/
2) https://docs.python.org/3.7/library/asyncio.html
'''

# used for receiving via OSC
import argparse
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
from .omnimidi import OmniMidi

class OmniCollider:

    def __init__(self, delay):
        self.delay = delay
        self.midi_evnt = []
        self.teensy = OmniMidi()
        self.d = dispatcher.Dispatcher()
        self.note_evnt_hist = dict()

        # dictionary holding all patches and their parameters.
        #     organization: self.patch_param_table[(synth, param_num)] = [param_name, default_val]]
        self.patch_param_table = dict()

        # dictionary holding all output devices and their index in SC.
        #     organization: self.out_dev_table[dev_num] = out_dev_name 
        self.out_dev_table = dict()

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

            param_arr = [param_name, param_default_val]
            if (synth, param_num) in self.patch_param_table:
                if not param_arr in self.patch_param_table[(synth, param_num)]:
                    self.patch_param_table[(synth, param_num)] = param_arr
            else:
                self.patch_param_table[(synth, param_num)] = param_arr       
        if event[0] == "/outDev":
            dev_num = event[1]
            dev_name = event[2]
            if dev_num not in self.out_dev_table:
                self.out_dev_table[dev_num] = dev_name
        print(event)

    async def loop(self):
        # sleep time
        for x in range(self.delay):
            await asyncio.sleep(0.001)

    async def init_main(self):
        rx = argparse.ArgumentParser()
        rx.add_argument("--ip", default="127.0.0.1", help="osc default ip")
        rx.add_argument("--port", type=int, default=7771, help="supercollider tx osc port")
        rx_args = rx.parse_args()
        server = osc_server.AsyncIOOSCUDPServer(
            (rx_args.ip, rx_args.port), self.d, asyncio.get_event_loop())
        transport, protocol = await server.create_serve_endpoint()
        await self.loop()
        transport.close()

    def receive(self):
        asyncio.run(self.init_main())

    def map_dispatcher(self, sc_variable):
        self.d.map(sc_variable, self.rx_handler)

    def transmit(self, command, control, *args):
        port = 57120
        if (command == "server"): port = 57110
        tx = argparse.ArgumentParser()
        tx.add_argument("--ip", default="127.0.0.1", help="osc default ip")
        tx.add_argument("--port", type=int, default=port, help="supercollider rx osc port")
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
