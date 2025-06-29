import socket
import threading

# Define constants
PORT = 5000
SERVER = '0.0.0.0' # listen on all interfaces
ADDR = (SERVER, PORT)

# create socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# global connections list
connections = set()

# single connection manager
def connection_manager(conn, addr):
    connections.add(conn) # add connection to active connection list
    while True:
        data = conn.recv(1024) # get data from client
        message = data.decode()
        if "exit" in message: # end chat
            connections.remove(conn) # remove client connection from list when done
            conn.close()
            return
        # else we transmit message to all chat members in active list except ourselves
        message = str(addr[1]) + ": " + message # add sender port number to message
        print(message) # log message to console
        for chat_member in connections:
            if chat_member != conn:
                chat_member.send(message.encode())

print("Server is listening on " + SERVER + ":" + str(PORT))
server.listen()

while True:
    connection, address = server.accept()
    print("New connection from ('" + address[0] + "', " + str(address[1]) + ")") # connection info
    # create thread for each connection
    thread = threading.Thread(target=connection_manager, args=(connection, address))
    thread.start()
