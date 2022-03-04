from server import Server

def start_server():
    server = Server()
    server.app.run('127.0.0.1', port='42042', debug=True)

if __name__ == "__main__":
    start_server()