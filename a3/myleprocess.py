import socket
import threading
import uuid
import csv
import json
import time

# get ip and port info from config
with open("config.txt", "r") as file:
    reader = csv.reader(file)
    config = list(reader)

# init global connection info with config file info
SERVER = config[0][0]
SERVER_PORT = config[0][1]
CLIENT_SERVER = config[1][0]
CLIENT_PORT = config[1][1]

# flag to wait on client connection
client_connected = threading.Event()

# global client connection init to null
CLIENT = None


class Message:
    uuid = uuid.uuid4()
    flag = 0

    # converts obj to JSON string with newline termination
    def convert_to_json(self):
        return json.dumps({
            "uuid": str(self.uuid),
            "flag": str(self.flag)
        }) + "\n"

    def print_message(self):
        return "UUID: " + str(self.uuid) + ", Flag: " + str(self.flag)


NODE_INFO = Message() # our nodes id info


# message sender function
def send_message(client_socket, message):
    try:
        client_socket.sendall(message.convert_to_json().encode())
    except OSError:
        print("Message Send Error")


# connects with client and sets global connection variable
def run_client():
    global CLIENT
    # establish connection with other server
    try:
        CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        CLIENT.connect((CLIENT_SERVER, CLIENT_PORT))
    except OSError:
        print("Client Connection Error")
        return
    client_connected.set() # set flag confirming client connection success


def run_server():
    global SERVER
    global SERVER_PORT

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((SERVER, SERVER_PORT))
    SERVER.listen()

    # accept one connection
    connection, address = SERVER.accept()

    # wait for client to confirm connection before proceeding
    while not client_connected.is_set():
        pass

    # send our id
    send_message(CLIENT, NODE_INFO)

    buffer = bytes()

    while True:
        data = connection.recv(1024)
        if not data:
            return # connection has been closed
        buffer += data # append data to buffer

        while b'\n' in buffer:
            # extract message data from buffer up to newline
            message, buffer = buffer.split(b'\n', 1)
            # process message



# start server in thread
server_thread = threading.Thread(target=run_server)
server_thread.start()

time.sleep(5) # wait 5 seconds before trying to connect client

client_thread = threading.Thread(target=run_client)
client_thread.start()

client_thread.join()
server_thread.join()


