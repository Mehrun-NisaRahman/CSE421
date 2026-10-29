import socket

# Server configuration
SERVER_PORT = 5050
BUFFER_SIZE = 16
ENCODING = 'utf-8'
DISCONNECT_SIGNAL = "False"

# Get server hostname and IP address
server_hostname = socket.gethostname()
server_ip = socket.gethostbyname(server_hostname)

print(f"Server Hostname: {server_hostname}")
print(f"Server IP Address: {server_ip}")

server_address = (server_ip, SERVER_PORT)

# Create a TCP socket, bind it and start listening
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen()

print(f"Server is running and listening on {server_ip}:{SERVER_PORT}")

def count_vowels(text):
    vowels = 'aeiouAEIOU'
    return sum(ch in vowels for ch in text)

while True:
    connection, client_address = server_socket.accept()
    print(f"Connection established with client: {client_address}")

    connected = True
    while connected:
        raw_msg_length = connection.recv(BUFFER_SIZE).decode(ENCODING)
        print(f"Raw message length from the client: {raw_msg_length}")

        if raw_msg_length:
            msg_length = int(raw_msg_length.strip())
            message = connection.recv(msg_length).decode(ENCODING)

            if message == DISCONNECT_SIGNAL:
                connection.send("Goodbye!".encode(ENCODING))
                print("Client requested disconnect. Closing connection.")
                connected = False
            else:
                vowel_count = count_vowels(message)
                if vowel_count == 0:
                    reply = "Not enough vowels"
                elif vowel_count <= 2:
                    reply = "Enough vowels I guess"
                else:
                    reply = "Too many vowels"

                print(f"Received message: {message}")
                print(f"Vowels counted: {vowel_count}")
                connection.send(reply.encode(ENCODING))
        else:
            # Empty recv() means the client closed without sending "False"
            print("Client disconnected without sending the disconnect signal.")
            connected = False

    connection.close()
    print("Closed connection with client.\n")
