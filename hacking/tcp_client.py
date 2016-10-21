import socket
import time, datetime

target_host = "ussandbox.gizwits.com"
target_port = 1883
internal_time = 660

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to Client
client.connect((target_host, target_port))

while True:
    # Send some data
    print datetime.datetime.now()
    print "Ready to send data."
    #client.send("GET / HTTP/1.1\r\nHost: baidu.com\r\n\r\n")
    print datetime.datetime.now()
    print client.getpeername
    # # # Response some data
    # # print "Waiting for response."
    # # response = client.recv(4096)
    # # Display the response
    # print response
    print datetime.datetime.now()
    print "Sent data and sleep."
    time.sleep(internal_time)
