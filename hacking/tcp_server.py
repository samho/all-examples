import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

# Create a socket object.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Binding the ip and port
server.bind((bind_ip, bind_port))

# Startup to listen with 5 connections
server.listen(5)

print "[*] Listening on %s:%d" % (bind_ip, bind_port)


# The thread for handling connection of client
def handle_client(client_socket):
    # Display the content from client
    request = client_socket.recv(1024)
    print "[*] Received: %s" % request
    # Response a packages
    client_socket.send("ACK!")
    client_socket.close()


while True:
    client, addr = server.accept()
    print "[*] Accepted connection from: %s:%d" % (addr[0], addr[1])

    # Suspend the client thread to process the data from client.
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()

