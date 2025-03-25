import socket
import threading

# Server Configuration
HOST = '127.0.0.1'  # Localhost
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server is listening on {HOST}:{PORT}...")

clients = {}  # Dictionary to store client sockets and their IDs
client_id_counter = 1  # Unique ID counter

def broadcast(message, sender_socket):
    """Send message to all clients except the sender."""
    for client_socket in clients.keys():
        if client_socket != sender_socket:
            try:
                client_socket.send(message)
            except:
                client_socket.close()
                del clients[client_socket]

def handle_client(client_socket, addr):
    """Handles messages from a client."""
    global client_id_counter
    client_id = client_id_counter  # Assign a unique ID
    client_id_counter += 1
    
    clients[client_socket] = client_id  # Store client ID
    client_socket.send(f"Your Client ID: {client_id}".encode())  # Send ID to client

    print(f"Client {client_id} connected from {addr}")

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"Client {client_id} says: {message}")
            broadcast(f"Client {client_id}: {message}".encode(), client_socket)
        except:
            break

    print(f"Client {client_id} disconnected.")
    del clients[client_socket]
    client_socket.close()

# Accept multiple client connections
while True:
    client_socket, addr = server_socket.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    thread.start()
