import os
import socket

def send_ping():
    HOST = '127.0.0.1' 
    PORT = 42042

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"Hello Mango")
        data = s.recv(1024)
        print(data.decode())

if __name__ == "__main__":
    send_ping()