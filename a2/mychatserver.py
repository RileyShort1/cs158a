import socket
import threading

# Define constants
PORT = 5000
SERVER = 'localhost'
ADDR = (SERVER, PORT)

# create socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# global connections list
connections = set()

# single connection manager
def connection_manager(conn, addr):
    connections.add(conn)

    while True:
        data = conn.recv(1024)
        message = data.decode()
        if "exit" in message: # end chat (need to adjust for case)
            connections.remove(conn) # remove client connection when done
            conn.close()
            return
        # else we transmit message to all chat members except ourselves
        message = str(addr[1]) + ": " + message # add sender port number
        print(message) # log message to console
        for chat_member in connections:
            if chat_member != conn:
                chat_member.send(message.encode())

print("Server is listening on " + SERVER + ":" + str(PORT))
server.listen()

while True:
    connection, address = server.accept()
    print("New connection from ('" + address[0] + "', " + str(address[1]) + ")")
    # create thread for connection
    thread = threading.Thread(target=connection_manager, args=(connection, address))
    thread.start()
