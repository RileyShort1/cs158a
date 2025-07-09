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
print("Server is: " + SERVER)
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

def json_string_to_message_obj(json_string):
    message = Message()
    message_data = json.loads(json_string)
    message.uuid = uuid.UUID(message_data["uuid"])
    message.flag = int(message_data["flag"])
    return message


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
        CLIENT.connect((CLIENT_SERVER, int(CLIENT_PORT)))
    except OSError as e:
        print(f"Client Connection Error: [Errno {e.errno}] {e.strerror} - {e}")
        return
    client_connected.set() # set flag confirming client connection success


def run_server():
    global SERVER
    global SERVER_PORT
    global CLIENT

    print("Server value = " + SERVER)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER, int(SERVER_PORT)))
    server.listen()

    # accept one connection
    connection, address = server.accept()

    # wait for client to confirm connection before proceeding
    while not client_connected.is_set():
        pass

    log_file = open("log.txt", "a")
    log_file.write("Sent: " + str(NODE_INFO.uuid) + ", flag=" + str(NODE_INFO.flag) + ", " + str(NODE_INFO.flag) + "\n")
    # send our id
    send_message(CLIENT, NODE_INFO)

    buffer = bytes()

    while True:
        data = connection.recv(1024)
        if not data:
            return # connection has been closed
        buffer += data # append data to buffer

        while b'\n' in buffer:
            # extract message data from buffer up to newline char
            message, buffer = buffer.split(b'\n', 1) # does not include newline
            # convert message to Message object
            received_message = json_string_to_message_obj(message.decode())

            if received_message.flag == 1:
                # leader has already been decided
                log_file.write("Received: uuid=" + str(received_message.uuid) + ", flag=" + str(received_message.flag) + ", " + str(received_message.flag) + "\n")
                log_file.write("Leader is decided to " + str(received_message.uuid) + "\n")
                send_message(CLIENT, received_message)
                connection.close()
                log_file.close()
                return


            if received_message.uuid > NODE_INFO.uuid:
                log_file.write("Received: uuid=" + str(received_message.uuid) + ", flag=" + str(received_message.flag) + ", greater, " + str(received_message.flag) + "\n")
                send_message(CLIENT, received_message) # forward message

            elif received_message.uuid == NODE_INFO.uuid:
                # we are the leader
                log_file.write("Leader is decided to " + str(NODE_INFO.uuid) + "\n")
                NODE_INFO.flag = 1 # mark as leader found
                log_file.write("Sent=" + str(NODE_INFO.uuid) + ", flag=" + str(NODE_INFO.flag) + ", equal, " + str(NODE_INFO.flag) + "\n")
                send_message(CLIENT, NODE_INFO)
                log_file.close()
                connection.close()
                return
            else:
                log_file.write("Ignored: uuid=" + str(received_message.uuid) + ", flag=" + str(received_message.flag) + " less, " + str(received_message.flag) + "\n")




# start server in thread
server_thread = threading.Thread(target=run_server)
server_thread.start()

time.sleep(5) # wait 5 seconds before trying to connect client

client_thread = threading.Thread(target=run_client)
client_thread.start()

client_thread.join()
server_thread.join()

if client_connected.is_set():
    CLIENT.close()



