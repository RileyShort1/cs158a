import socket
import ssl

HOSTNAME = 'www.google.com'
PORT = 443

context = ssl.create_default_context()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOSTNAME, PORT))

ssl_socket = context.wrap_socket(client, server_hostname=HOSTNAME)
print("Socket Created")

request = 'GET / HTTP/1.1'
ssl_socket.sendall(request.encode())
print("Sent Request")

print(ssl_socket.recv(1024).decode())
print("Recv Done")