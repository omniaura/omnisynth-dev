"""
This server is an API around the OSC functionality and state managament 
for clients to utilize.
"""

import socket

class Server:

    def __init__(self):
        self.response = []

    def request_handler(self, request):
        response = '{ "data" : "%s" }' % request
        return response

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', 42042))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    response = self.request_handler(str(data.decode()))
                    conn.sendall(response.encode())


if __name__ == "__main__":
    
    server = Server()
    while True:
        server.start_server()
