import socket

serverName = '127.0.0.1'
portNumber = 5000

#TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((serverName, portNumber))

# get user input and send to server
message = input("Input lowercase sentence: ")
client.send(message.encode()) # send message to server

length = int(message[0:2])
response = bytes()

# get full response
while len(response) < length:
    response += client.recv(64)

# print result string from server
print("From Server: " + response.decode())
client.close()



