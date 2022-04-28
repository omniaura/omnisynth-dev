from server import Server
from gevent.pywsgi import WSGIServer
import subprocess
import socket 
from flask import g

def start_server():
    server = Server()
    subprocess.Popen(['python', 'modules/omni_instance.py'])
    http_server = WSGIServer(('localhost', 42042), server.app)
    http_server.serve_forever()

if __name__ == "__main__":
    start_server()
    