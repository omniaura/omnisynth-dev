from server import Server
from gevent.pywsgi import WSGIServer
import subprocess
import socket
from flask import g

PORT = 42042


def start_server():
    print(f"Starting Omnisynth Flask server on port {PORT}...")
    server = Server()
    http_server = WSGIServer(('localhost', 42042), server.app)
    http_server.serve_forever()
    print(f"Server started!")

    print("Starting OmniSynth instance in the background...")
    subprocess.Popen(['python', 'modules/omni_instance.py'])
    print("Omnisynth instance running!")


if __name__ == "__main__":
    start_server()
