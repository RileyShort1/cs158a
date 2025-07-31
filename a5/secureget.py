import re
import socket
import ssl

# define hostname and port
HOSTNAME = 'www.google.com'
PORT = 443

context = ssl.create_default_context() # default ssl config

# create standard socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOSTNAME, PORT))

# wrap socket
ssl_socket = context.wrap_socket(client, server_hostname=HOSTNAME)
print("Socket Created")

# define GET request
request = 'GET / HTTP/1.1\r\n' + 'Host: ' + str(HOSTNAME) + '\r\n\r\n'
print(request)
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

file = open("response.html", 'w')
file.write(cleaned_html)





