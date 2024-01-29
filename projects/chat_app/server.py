import socket
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 12345

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

# List to store connected clients
clients = []

# Function to broadcast messages to all clients
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                # Remove the client if unable to send the message
                clients.remove(client)

# Function to handle a client's connection
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            broadcast(message, client_socket)
        except:
            # Remove the client if there is an error
            clients.remove(client_socket)
            break

# Main loop to accept incoming connections
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connected with {client_address}")
    clients.append(client_socket)
    # Start a new thread to handle the client's connection
    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()
