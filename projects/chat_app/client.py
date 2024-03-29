import socket
import threading

# Client configuration
HOST = '127.0.0.1'
PORT = 12345

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))

# Function to send messages
def send_message():
    while True:
        message = input()
        client_socket.send(message.encode())

# Function to receive messages
def receive_message():
    while True:
        try:
            message = client_socket.recv(1024)
            print(message.decode())
        except:
            # Handle any errors while receiving messages
            break

# Start two threads for sending and receiving messages
send_thread = threading.Thread(target=send_message)
receive_thread = threading.Thread(target=receive_message)

send_thread.start()
receive_thread.start()
