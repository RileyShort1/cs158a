import queue
import socket
import threading
import uuid
import csv
import json
import time
import sys
from queue import Queue

# default looks for config file in working directory
config_file_path = "config.txt"
log_file_path = "log.txt"

# if command line argument path is provided use that
if len(sys.argv) > 1:
    config_file_path = sys.argv[1]
if len(sys.argv) > 2:
    log_file_path = sys.argv[2]

# get ip and port info from config
with open(config_file_path, "r") as file:
    reader = csv.reader(file)
    config = list(reader)

# init global connection info with config file info
SERVER_IP = config[0][0]
SERVER_PORT = config[0][1]
CLIENT_CONN_IP = config[1][0]
CLIENT_CONN_PORT = config[1][1]

# Server will place all messages here
# Queue has built in thread safety
MESSAGES = Queue()

# flag for client and server connection status
client_connected = threading.Event()
server_connected = threading.Event()

leader_found = threading.Event()

log_file = open(log_file_path, "w")

log_lock = threading.Lock()
def log(message):
    global log_file
    with log_lock:
        log_file.write(message)
        log_file.flush()

class Message:
    # converts obj to JSON string with newline termination
    def convert_to_json(self):
        return json.dumps({
            "uuid": str(self.uuid),
            "flag": str(self.flag)
        }) + "\n"

    def to_string(self):
        return "uuid=" + str(self.uuid) + ", flag=" + str(self.flag)

    def __init__(self, json_string=None):
        if json_string is None:
            self.uuid = uuid.uuid4()
            self.flag = 0
        else:
            message_data = json.loads(json_string)
            self.uuid = uuid.UUID(message_data["uuid"])
            self.flag = int(message_data["flag"])


NODE_INFO = Message() # our nodes id info

LEADER_ID = None # var for tracking leader id

# sends message obj using socket
def send_message(client_socket, message):
    try:
        client_socket.sendall(message.convert_to_json().encode())
        log("Sent: " + message.to_string() + "\n")
    except OSError:
        print("Message Send Error")


# starts server and begins placing incoming messages into queue
def accumulate_messages():
    global SERVER_IP
    global SERVER_PORT
    global MESSAGES

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, int(SERVER_PORT)))
    server.listen()

    connection, address = server.accept() # accept one connection
    server_connected.set() # set flag to true

    buffer = bytes()
    while not leader_found.is_set():
        try:
            data = connection.recv(1024)
        except socket.error:
            print("Error receiving data in accumulate_messages() - server connection terminated")
            server_connected.clear() # set flag to false
            connection.close()
            break
        if not data: # connection has been closed
            server_connected.clear() # set flag to false
            connection.close()
            break
        else:
            buffer += data # append data to buffer
            while b'\n' in buffer: # extract message data (does not include \n
                message, buffer = buffer.split(b'\n', 1)
                message_obj = Message(message.decode())
                MESSAGES.put(message_obj) # enqueue message
                equality = "less" if message_obj.uuid < NODE_INFO.uuid else "greater" if message_obj.uuid > NODE_INFO.uuid else "equal"
                log("Received: " + message_obj.to_string() + ", " + equality + ", " + str(NODE_INFO.flag) + "\n") # log received message


# function processes message obj according to LE algorithm
def process_messages(client, message):
    global LEADER_ID

    if message.flag == 1: # leader has already been decided
        NODE_INFO.flag = 1 # mark as leader found
        log("Leader is decided to " + str(message.uuid) + "\n")
        send_message(client, message)
        leader_found.set()
        LEADER_ID = str(message.uuid) # save leader ID
        return

    if message.uuid > NODE_INFO.uuid:
        send_message(client, message) # forward message

    elif message.uuid == NODE_INFO.uuid:
        # we are the leader
        NODE_INFO.flag = 1
        log("Leader is decided to " + str(message.uuid) + "\n")
        send_message(client, NODE_INFO)
        leader_found.set()
        LEADER_ID = str(NODE_INFO.uuid) # save leader ID
        return
    else:
        log("Ignored: " + message.to_string() + "\n")


# connects with client and sets global connection variable
def run_client(delay):
    time.sleep(delay)
    try: # establish connection with other server
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((CLIENT_CONN_IP, int(CLIENT_CONN_PORT)))
    except OSError as e:
        print("Client Connection Error in run_client()")
        return
    client_connected.set() # set flag

    # send init message
    send_message(client, NODE_INFO)

    # get message and process
    while not leader_found.is_set():
        try:
            message = MESSAGES.get(block=False)
            process_messages(client, message)
        except queue.Empty:
            continue

    client_connected.clear()
    client.close()


# start server in thread
server_thread = threading.Thread(target=accumulate_messages)
server_thread.start()

# start client
client_thread = threading.Thread(target=run_client, args=(5,))
client_thread.start()


client_thread.join()
server_thread.join()
log("\nLeader is " + str(LEADER_ID))

log_file.close()
