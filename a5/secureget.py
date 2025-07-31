import re
import socket
import ssl

HOSTNAME = 'www.google.com'
PORT = 443

context = ssl.create_default_context()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOSTNAME, PORT))

ssl_socket = context.wrap_socket(client, server_hostname=HOSTNAME)
print("Socket Created")

request = 'GET / HTTP/1.1\r\n\r\n'
ssl_socket.sendall(request.encode())

response = bytes()
chunk = bytes()
while True:
    try:
        chunk = ssl_socket.recv(1024)
        response += chunk # add to response message
        if b'0\r\n\r\n' in chunk:
            break
    except OSError:
        print("Connection Error")

response_string = response.decode()
html = response_string[response_string.find('<!doctype html>'):]
cleaned_html = re.sub('[0-9a-fA-F]+\r\n', '', html) # sub out chunked data markers


file = open("html_data.html", 'w')
file.write(cleaned_html)





