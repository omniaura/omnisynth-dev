"""
This server is an API around the OSC functionality and state managament 
for clients to utilize.
"""

# import socket

from constants import OMNISYNTH_PATH
from omnisynth import omni

from flask import Flask
from flask import request

app = Flask(__name__)
OmniSynth = omni.Omni()


# postman as POST Test
@app.route("/", methods=['POST'])
def post_handler():
    return "<p>Hello, World!</p>"


@app.route("/patches", methods=['POST'])
def omnisynth_handler():
    requests = request.args
    if 'compileAllPatches' in requests:

        OmniSynth.sc_compile(OMNISYNTH_PATH+"patches") # compiles all synthDefs.
        OmniSynth.synth_sel("tone1", OMNISYNTH_PATH) # selects first patch.
        return "<p>Compiling all synth patches</p>"

    elif 'fileName' in requests: # assume full path (client must follow!)

        fname = str(request.args.get('fileName'))
        OmniSynth.sc_compile(fname)
        return f"<p>Compiled {fname}</p>"

    else:

        return "<p>Invalid Query. Must provide compileAllPatches or fileName.</p>"


class Server():

    def __init__(self):
        self.app = app

        
    
        


if __name__ == "__main__":
    
    server = Server()
