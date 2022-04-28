'''
Boots the OmniSynth Server for API calls and starts an instance of SuperCollider (OmniSynth DSP)
'''

import gevent.subprocess as subprocess

# starts the server as a subprocess
def start_server():
    subprocess.call(['python', 'modules/start_server.py'])
    
    
if __name__ == "__main__":
    start_server()
