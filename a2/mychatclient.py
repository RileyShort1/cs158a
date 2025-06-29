import socket
import threading

SERVER = 'localhost' # change to servers IP here
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

# thread event signals connection status
disconnected = threading.Event()

# runs until server disconnects us
def refresh_chat():
    while not disconnected.is_set():
        try:
            chat = client.recv(1024)
            print(chat.decode())
            if chat == b'': # server sends end signal
                disconnected.set()
        except OSError:
            print("Connection Error ... disconnected")
            disconnected.set()


# waits on user input and sends to server
def send():
    while not disconnected.is_set(): # while connection is still alive
        message = input() # blocking function call
        try:
            client.send(message.encode())
            if "exit" in message:
                disconnected.set()
        except OSError:
            print("Connection Error ... disconnected")
            disconnected.set()


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