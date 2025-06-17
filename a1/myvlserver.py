import socket
import threading

# Define constants
PORT = 5000
SERVER = "0.0.0.0"
ADDR = (SERVER, PORT)

# init socket and bind server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def connection_manager(conn, addr):
    try: # ensure valid str to int conversion
        message_len = int(conn.recv(2).decode())  # get message length (first two bytes)
    except ValueError:
        message_len = 0
    message = bytes() # message accumulator obj

    # print connection info
    print("Connected from: " + str(addr[0]))
    print("msg_len: " + str(message_len))

    while len(message) < message_len:
        data = conn.recv(64) # receive data with 64 byte buffer
        message += data # add data to message object

    message = message[0:message_len] # trim message past limit
    response = message.decode().upper()
    conn.send(response.encode()) # send all caps response
    conn.close()
    print("processed: " + message.decode())
    print("msg_len_sent: " + str(len(response)))
    print("Connection closed\n...")

print("Server Starting...")
server.listen()
while True: # server runs until manual termination
    connection, address = server.accept()
    # create thread so multiple clients can be served simultaneously (each on unique thread)
    thread = threading.Thread(target=connection_manager, args=(connection,address))
    thread.start()



