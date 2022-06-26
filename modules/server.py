"""
This server is an API around the OSC functionality and state managament 
for clients to utilize.

author: Omar Barazanji (omar@omniaura.co)
"""

import platform
import omni_instance
from constants import OMNISYNTH_PATH, SUPERCOLLIDER_PROCESS_NAMES
import re
import redis
import subprocess
import psutil
from flask import Flask
from flask import request
import json

app = Flask(__name__)
r = redis.Redis.from_url(url='redis://127.0.0.1:6379/0')

OI = omni_instance.OmniInstance()


OS = 'Windows'
if platform.system() == 'Linux':
    OS = 'Linux'
elif platform.system() == 'Darwin':
    OS = 'Darwin'

r.set('serverStatus', 'off')

# postman as POST Test


@app.route("/", methods=['POST'])
def post_handler():
    return "<p>Hello, World!</p>"

# making requests to the OmniSynth instance


@app.route("/omnisynth", methods=['POST', 'GET'])
def omnisynth_handler():
    requests = request.args

    if request.method == "POST":
        if 'mapKnob' in requests:
            req = json.loads(requests['mapKnob'])
            knob_source = req['knobSource']
            knob_chan = req['knobChan']
            filter_name = req['filterName']
            OI.OmniSynth.map_knob((knob_source, knob_chan), filter_name)
            return f"<p>Mapping {knob_source, knob_chan} to {filter_name}</P"

    if request.method == "GET":
        if 'getKnobTable' in requests:
            knob_table = r.get('knobTable')
            return knob_table


@app.route("/patterns", methods=['POST', 'GET'])
def patterns_handler():
    requests = request.args

    if request.method == 'POST':
        if 'startPattern' in requests:
            pattern = str(request.args.get('startPattern'))
            OI.OmniSynth.pattern_sel(pattern, 'compile', OMNISYNTH_PATH)
            OI.OmniSynth.pattern_sel(pattern, 'start')
            return f"<p>Starting {pattern}</p>"

        elif 'stopPattern' in requests:

            pattern = str(request.args.get('stopPattern'))
            OI.OmniSynth.pattern_sel(pattern, 'stop')
            return f"<p>Stopping {pattern}</p>"

        elif 'bpmSet' in requests:
            value = str(request.args.get('bpmSet'))
            OI.OmniSynth.pattern_param_sel('bpm', value)
            return f"<p>Setting current pattern's bpm to {value}</p>"

        elif 'synthSet' in requests:
            synth = str(request.args.get('synthSet'))
            OI.OmniSynth.pattern_param_sel('synth', synth)
            return f"<p>Setting current pattern's synth to {synth}</p>"
    elif request.method == 'GET':
        pass


@app.route("/patches", methods=['POST', 'GET'])
def patches_handler():
    requests = request.args

    if request.method == 'POST':
        if 'compileAllPatches' in requests:
            OI.compile_patches()
            return "<p>Compiling All Patches</p>"

        elif 'patchName' in requests:

            patch = str(request.args.get('patchName'))
            OI.OmniSynth.synth_sel(patch, OMNISYNTH_PATH)
            return f"<p>Compiled {patch}</p>"

        else:

            return "<p>Invalid Query. Must provide compileAllPatches or patchName.</p>"

    elif request.method == 'GET':
        if 'patchTable' in requests:
            table = r.get('patchTable')
            return json.loads(table)

        elif 'patchName' in requests:
            table = r.get('patchTable')
            patchTable = json.loads(table)
            patch = patchTable.get(request.args.get('patchName'))
            return patch
    else:

        return "<p>Invalid Query. Must provide compileAllPatches or patchName.</p>"


# start supercollider server and simulates the GUI's event loop as `While True`.
@app.route("/supercollider", methods=['POST', 'GET'])
def supercollider_handler():
    requests = request.args
    if request.method == "POST":
        if 'startServer' in requests:
            r.set('serverStatus', 'starting')
            sc_main = OMNISYNTH_PATH + "main.scd"
            if 'Darwin' in OS:
                subprocess.Popen(
                    ["/Applications/SuperCollider.app/Contents/MacOS/sclang", sc_main])
            else:
                subprocess.Popen(["sclang", sc_main])
            return "<p>Starting server</p>"


        elif 'killServer' in requests:

            OI.OmniSynth.exit_sel()  # kills scsynth
            for proc in psutil.process_iter():
                if proc.name().lower().strip(".exe") in SUPERCOLLIDER_PROCESS_NAMES:
                    print(f'killing process {proc.name()}')
                    proc.kill()
            r.set('serverStatus', "off")

            return "<p>Server killed</p>"
        else:

            return "<p>Invalid Query. Must provide startServer or killServer.</p>"

    elif request.method == "GET":
        if 'getOutDev' in requests:
            out_devices = r.get('outDevTable')
            return out_devices
        elif 'serverStatus' in requests:
            status = r.get('serverStatus')
            return json.dumps({"status": status.decode()})


class Server():

    def __init__(self):
        self.app = app


if __name__ == "__main__":

    server = Server()
