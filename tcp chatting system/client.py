import socket
import threading

# Server details
HOST = '127.0.0.1'  # Must match the server's IP
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Receive the assigned Client ID
client_id = client_socket.recv(1024).decode()
print(client_id)  # Display Client ID

def receive_messages():
    """Continuously receives messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(f"\n{message}")
        except:
            print("Disconnected from server.")
            client_socket.close()
            break

# Start receiving messages in a separate thread
threading.Thread(target=receive_messages, daemon=True).start()

# Sending messages to the server
while True:
    msg = input("Enter message: ")
    client_socket.send(msg.encode())
