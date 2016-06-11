import socket

target_host = "127.0.0.1"
target_port = 9999

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to Client
client.connect((target_host, target_port))

# Send some data
client.send("GET / HTTP/1.1\r\nHost: baidu.com\r\n\r\n")

# Response some data
response = client.recv(4096)

# Display the response
print response
