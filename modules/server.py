"""
This server is an API around the OSC functionality and state managament 
for clients to utilize.
"""

import redis
import subprocess
from flask_socketio import SocketIO
from flask import Flask
from flask import request

app = Flask(__name__)
r = redis.Redis.from_url(url='redis://127.0.0.1:6379/0')

from constants import OMNISYNTH_PATH
import omni_instance
OI = omni_instance.OmniInstance()

# handles communication with the omnisytnth service
def omnisynth_service(msg):
    pass

# postman as POST Test
@app.route("/", methods=['POST'])
def post_handler():
    return "<p>Hello, World!</p>"


# used to test if omnisynth service is running
@app.route("/omnisynth", methods=['POST', 'GET'])
def omnisynth_handler():
    requests = request.args
    if request.method == "POST":
        
        return f"<p>POST to OmniSynth Instance</p>"


@app.route("/patches", methods=['POST', 'GET'])
def patches_handler():
    requests = request.args

    if request.method == 'POST':
        if 'compileAllPatches' in requests:
            OI.compile_patches()
            return "<p>Compiling All Patches</p>"

        elif 'patchName' in requests: # assume full path (client must follow!)

            patch = str(request.args.get('patchName'))
            # OmniSynth.synth_sel(patch, OMNISYNTH_PATH)
            return f"<p>Compiled {patch}</p>"
        
        else:

            return "<p>Invalid Query. Must provide compileAllPatches or patchName.</p>"

    elif request.method == 'GET':
        if 'patchTable' in requests:
            table = r.get('patchTable')
            return table
    else:

        return "<p>Invalid Query. Must provide compileAllPatches or patchName.</p>"
    




# start supercollider server and simulates the GUI's event loop as `While True`.
@app.route("/supercollider", methods=['POST', 'GET'])
def supercollider_handler():
    requests = request.args
    if request.method == "POST":
        if 'startServer' in requests:
            sc_main = OMNISYNTH_PATH + "main.scd"
            subprocess.Popen(["sclang", sc_main])
            # initialize OmniSynth instance
            # OmniSynth.sc_compile(OMNISYNTH_PATH+"patches") # compiles all synthDefs.
            # OmniSynth.synth_sel("tone1", OMNISYNTH_PATH) # selects first patch.
            # OmniSynth.midi_learn_on = True # turn on midi learn.

            return "<p>Started server</p>"

        elif 'killServer' in requests:

            # OmniSynth.exit_sel()
            return "<p>Server killed</p>"

        else:

            return "<p>Invalid Query. Must provide startServer or killServer.</p>"
            
    elif request.method == "GET":
        pass
        # print(OmniSynth.sc.patch_param_table)
        # return OmniSynth.sc.patch_param_table



class Server():

    def __init__(self):
        self.app = app


if __name__ == "__main__":
    
    server = Server()
