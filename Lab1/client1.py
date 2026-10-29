import socket

# Client configuration
SERVER_PORT = 5050
BUFFER_SIZE = 16
ENCODING = 'utf-8'
DISCONNECT_SIGNAL = "False"

# Get client hostname and IP address
client_hostname = socket.gethostname()
client_ip = socket.gethostbyname(client_hostname)

print(f"Client Hostname: {client_hostname}")
print(f"Client IP Address: {client_ip}")

# Server runs on the same PC, so we use our own IP as the server address
server_address = (client_ip, SERVER_PORT)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

def send_message(message):
    encoded_message = message.encode(ENCODING)

    # Fixed-length (16 byte) header with the message length
    message_length = str(len(encoded_message)).encode(ENCODING)
    padded_length = message_length + b' ' * (BUFFER_SIZE - len(message_length))

    client_socket.send(padded_length)
    client_socket.send(encoded_message)

    response = client_socket.recv(2048).decode(ENCODING)
    print(f"Server response: {response}")

# Inform the server of the client's IP and device name
intro_message = f"Client IP: {client_ip}, Client Name: {client_hostname}"
send_message(intro_message)

send_message(DISCONNECT_SIGNAL)
client_socket.close()
print("Disconnected from server.")
