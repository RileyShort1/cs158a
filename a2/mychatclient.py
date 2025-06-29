import socket
import threading

SERVER = '10.0.0.210' # change to servers IP here
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

end = threading.Event()

# runs until server disconnects us
def refresh_chat():
    while not end.is_set():
        chat = client.recv(1024)
        if chat == b'':
            end.set()
            return
        print(chat.decode())

# waits on user input and sends to server
def send():
    while not end.is_set(): # while connection is still alive
        message = input() # blocking function call
        client.send(message.encode())
        if "exit" in message:
            end.set()
            return

def enter_chat():
    print("Connected to chat server. Type 'exit' to leave.")
    chat_refresh_thread = threading.Thread(target=refresh_chat)
    chat_refresh_thread.start() # will run until connection closed

    message_sender_thread = threading.Thread(target=send)
    message_sender_thread.start() # will run until 'exit' is typed

    chat_refresh_thread.join()
    message_sender_thread.join()

    client.close()
    print("Disconnected from server")

enter_chat()