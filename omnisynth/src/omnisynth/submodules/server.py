"""
This server is an API around the OSC functionality and state managament 
for clients to utilize.
"""

# import socket

from flask import Flask
app = Flask(__name__)


# postman as POST Test
@app.route("/", methods=['POST'])
def post_handler():
    return "<p>Hello, World!</p>"

class Server:

    def __init__(self):
        self.response = []
        
    
if __name__ == "__main__":
    
    server = Server()
