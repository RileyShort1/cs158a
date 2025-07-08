import socket
import threading
import uuid

class Message:
    id = uuid.uuid4()
    flag = 0


# client connection code
def run_client():
    server = 'localhost'
    port = 5000

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server, port))

def run_server():
    # add server connection code here
    port = 5001
    server = '0.0.0.0' # listen on all interfaces

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server, port))
    server.listen()

    while True:
        # accept one connection
        connection, address = server.accept()




# begin separate threads for client and server
client_thread = threading.Thread(target=run_client)
server_thread = threading.Thread(target=run_server)

client_thread.start()
server_thread.start()


