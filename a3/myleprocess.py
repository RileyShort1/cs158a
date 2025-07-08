import socket
import threading
import uuid
import csv
import json

# get ip and port info from config
with open("config.txt", "r") as file:
    reader = csv.reader(file)
    config = list(reader)

# init global connection info with config file info
SERVER = config[0][0]
SERVER_PORT = config[0][1]
CLIENT_SERVER = config[1][0]
CLIENT_PORT = config[1][1]


class Message:
    uuid = uuid.uuid4()
    flag = 0

    # converts obj to JSON string with newline termination
    def convert_to_json(self):
        return json.dumps({
            "uuid": str(self.uuid),
            "flag": str(self.flag)
        }) + "\n"

NODE_INFO = Message()
#print("UUID: " + str(NODE_INFO.uuid) + ", Flag: " + str(NODE_INFO.flag))

print(repr(NODE_INFO.convert_to_json()))

# client connection code
def run_client():
    global CLIENT_SERVER
    global CLIENT_PORT

    # establish connection with server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((CLIENT_SERVER, CLIENT_PORT))

    # send id value as first step
    # JSON formatted Message obj encoded to bytes
    client.sendall(NODE_INFO.convert_to_json().encode())



def run_server():
    global SERVER
    global SERVER_PORT

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((SERVER, SERVER_PORT))
    SERVER.listen()

    # accept one connection
    connection, address = SERVER.accept()




# begin separate threads for client and server
client_thread = threading.Thread(target=run_client)
server_thread = threading.Thread(target=run_server)

#client_thread.start()
#server_thread.start()

#client_thread.join()
#server_thread.join()


