import socket

serverName = '127.0.0.1'
portNumber = 5000

#TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((serverName, portNumber))

message = input("Input lowercase sentence: ")
client.send(message.encode()) # send message to server

length = int(message[0:2])
response = bytes()

while len(response) < length:
    response += client.recv(64)

print("From Server: " + response.decode())
client.close()



