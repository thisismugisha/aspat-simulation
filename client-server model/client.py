import socket
import handle_files
import pickle
import os
import shutil
import threading
import re

# Variables required for file manipulation
pattern = r',?([0-9]+),?'
temp_dir = "./temp_dir/"
temp_header_file = temp_dir + "temp_header_file.txt"
temp_binary_file = temp_dir + "temp_binary_file.txt"

# Variables required for socket connection
PC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = "172.20.10.2"
PORT = 3542
FORMAT = "utf-8"
HEADER = 2048
DISCONNECT = "DISCONNECT"

quiting = False

def rm_temp_dir(temp_dir):
    print("deleting the temporary folder")
    shutil.rmtree(temp_dir)
    print("deleted")

def start():
    os.makedirs(os.path.dirname(temp_dir), exist_ok=True) # create/open temporary directory
    print("[Temporary directory] it exists now")

    # def open_temp_files(exists):
    exists = os.path.isfile(temp_header_file) and os.path.isfile(temp_binary_file) # check if there are temporary header and binary files

    if exists:
        # Both temporary files are opened
        with open(temp_header_file, "r+") as header_file, open(temp_binary_file, "a+") as binary_file:
            # --------------------------------------- header file ---------------------------------------
            print("[Header] reading the header file")
            header_string = header_file.read() # Read what's in it
            print(f"header string: {header_string}")
            header = [int(i) for i in re.findall(pattern, header_string)] # turn string back to a list (except the file name)
            header.append(re.findall(r'\'?.\'?$', header_string)[0]) # add the file name
            print("[Header] Unpacking the header")
            source, destination, packet_number, total_packets, acknowledged_data, dataoffset, window, crc32, file_path = header # Unbox all the variables

            try:
                while True:
                    try:
                        acknowledged_data = int(input(f"How should the transfer be? Reliable[1] or unreliable[0]: "))
                        break
                    except ValueError:
                        print(f"The input is invalid. Please write 1(one) or 0(zero)")
                        continue

                PC.connect((IP, PORT)) # connect to the server
                connected = True                

                header = [source, destination, packet_number, total_packets, acknowledged_data, dataoffset, window, crc32, file_path]                
                PC.send(pickle.dumps(header))
                print("[Request] sent the header")
                while connected:
                    try:
                        try:
                            received = PC.recv(2048)
                        except (KeyboardInterrupt, ConnectionResetError):
                            connected = False
                            print(f"[Disconnected] connection closed")
                            rm_temp_dir(temp_dir)
                            return

                        if received:
                            received = pickle.loads(received)
                            if received == DISCONNECT:
                                connected = False
                                print(f"[Disconnected] connection closed")
                                rm_temp_dir(temp_dir)
                                return

                            else:
                                # print(received)
                                source, destination, packet_number, total_packets, acknowledged_data, dataoffset, window, crc32, file_path = received # Unbox all the variables
                                print(f"\n[ASPAT header] created the header: \nsource: {source}, destination: {destination}, packet_number: {packet_number}, total_packets: {total_packets}, acknowledged_data: {acknowledged_data}, dataoffset: {dataoffset}, window: {window}, crc32: {crc32}, file_path: {file_path}")
                                for packet in range(packet_number, total_packets):
                                    received = PC.recv(2048)
                                    received = pickle.loads(received)
                                    source, destination, packet_number, total_packets, acknowledged_data, dataoffset, window, crc32, file_path, data = received # Unbox all the variables
                                    if acknowledged_data == 1:
                                        # Add to the binary file
                                        binary_file.seek(0, 2) # Go to the end of the file
                                        binary_file.write(data) # Append new content at the end of the file

                                        binary_file.seek(0) # Go to the beginning of the file
                                        file_data = binary_file.read() # Read from the beginning
                                        acknowledged_data = len(file_data)
                                        
                                        # Update the header file
                                        header_list = [source, destination, packet_number, total_packets, acknowledged_data, dataoffset, window, crc32, file_path]
                                        header = ",".join(str(s) for s in header_list)
                                        header_file.truncate(0) # Delete what was in it
                                        header_file.seek(0)
                                        header_file.write(header) # Write new content

                                        # Send the header
                                        PC.send(pickle.dumps(header)) # Pickle and send the header to acknowledge the reception of the packet

                                        print(f"[Packet count] Received {(packet + 1)} of {total_packets}\n\n")
                                        print(header, data)
                                    else:
                                        # Add to the binary file
                                        binary_file.seek(0, 2) # Go to the end of the file
                                        binary_file.write(data) # Append new content at the end of the file
                                        
                                        # Update the header file
                                        header_list = [source, destination, packet_number, total_packets, acknowledged_data, dataoffset, window, crc32, file_path]
                                        header = ",".join(str(s) for s in header_list)
                                        header_file.truncate(0) # Delete what was in it
                                        header_file.seek(0)
                                        header_file.write(header) # Write new content

                                        print(header, data)

                        """ binary_file.seek(0) # Go to the beginning of the file
                        file_data = binary_file.read() # Read from the beginning

                        header_string = header_file.read() # Read what's in it
                        header = [int(i) for i in re.findall(pattern, header_string)] # turn string back to a list (except the file name)
                        file_path = re.findall(r'\'?.\'?$', header_string)[0] # Retrieve the file path
                        header.append(file_path) # add the file path

                        # Get the file name
                        filename_pattern = '[^/]+$' # Match any 1 or more characters that is not a forward slash till the end of the string
                        file_name = re.search(filename_pattern, file_path).group()
                        handle_files.binary_to_file(file_name, file_data) """

                        print("Going to the beginning of the binary file")
                        binary_file.seek(0) # Go to the beginning of the file
                        file_data = binary_file.read() # Read from the beginning
                        print(f"file data: {file_data}")
                        
                        print("Reading the header file")
                        header_string = header_file.read() # Read what's in it
                        print(f"header string: {header_string}")
                        header = [int(i) for i in re.findall(pattern, header_string)] # turn string back to a list (except the file name)
                        print(f"header: {header}")
                        file_path = re.findall(r'[^,]+$', header_string)[0] # Retrieve the file path
                        print(f"file path: {file_path}")
                        header.append(file_path) # add the file path

                        # Get the file name
                        filename_pattern = '[^/]+$' # Match any 1 or more characters that is not a forward slash till the end of the string
                        file_name = re.search(filename_pattern, file_path).group()
                        print(f"file name {file_name}")
                        handle_files.binary_to_file(file_name, file_data)
                        print("file created")

                        delete = input("Delete the temporary file? [0] for no, [1] for yes")
                        if delete == 1:
                            rm_temp_dir(temp_dir)

                    except (KeyboardInterrupt, ConnectionResetError):
                        print(f"[Disconnected] connection closed\n")
                        print("Exiting...")
                        connected = False
            except ConnectionRefusedError:
                print("\nCouldn\'t connect. Exiting\n")
                return
            
            # packet_number = 0
            # # binary_header_list = [source, destination, packet_number, total_packets, acknowledged_data, dataoffset, window, crc32]
            # binary_header = ",".join(str(s) for s in binary_header_list) # turn to a string
            # header_file.truncate(0) # Delete what was in it
            # header_file.write(binary_header) # Write new content
            # header_file.seek(0) # Go to the beginning of the file
            # header_string = header_file.read() # Read from the beginning
            # header = [int(i) for i in re.findall(pattern, header_string)] # turn string back to a list
            # print(f"header after: {header}\n")

            # --------------------------------------- data file ---------------------------------------
            print("\nreading the binary file")
            binary_file.seek(0) # Go to the beginning of the file
            file_data = binary_file.read() # Read from the beginning
            print(f"binary file: {file_data}\n")

            binary_file.seek(0, 2) # Go to the end of the file
            binary_file.write(str(input("Write what you wanna add to the binary file: "))) # Append new content at the end of the file
            print("added to the binary")
            binary_file.seek(0) # Go to the beginning of the file
            file_data = binary_file.read() # Read from the beginning
            print(f"new binary file: {file_data}\n")
    else:        
        with open(temp_header_file, "w") as header_file, open(temp_binary_file, "x"):
            header_ = [0, 0, 0, 0, 0, 192, 3, 0, "_"]
            header = ",".join(str(s) for s in header_) # turn to a string
            header_file.write(header)
            print(f"[Temp files] Created the temporary files {header}")
        
        start()

    """ try:
        PC.connect((IP, PORT))
        connected = True
        request = (0, 3)
        PC.send(pickle.dumps(request))
        print("sent the request")
        while connected:
            try:
                try:
                    received = PC.recv(2048)
                except (KeyboardInterrupt, ConnectionResetError):
                    connected = False
                    print(f"[Disconnected] connection closed")
                if received:
                    received = pickle.loads(received)
                    if received == DISCONNECT:
                        connected = False
                        print(f"[Disconnected] connection closed")
                    else:
                        print(received)
            except (KeyboardInterrupt, ConnectionResetError):
                print(f"[Disconnected] connection closed\n")
                print("Exiting...")
                connected = False
    except ConnectionRefusedError:
        print("\nCouldn\'t connect\n") """

threading.Thread(target=start, daemon=True).start()
""" with open(temp_header_file, "r+") as header_file, open(temp_binary_file, "a+") as binary_file:
    print("Going to the beginning of the binary file")
    binary_file.seek(0) # Go to the beginning of the file
    file_data = binary_file.read() # Read from the beginning
    print(f"file data: {file_data}")
    
    print("Reading the header file")
    header_string = header_file.read() # Read what's in it
    print(f"header string: {header_string}")
    header = [int(i) for i in re.findall(pattern, header_string)] # turn string back to a list (except the file name)
    print(f"header: {header}")
    file_path = re.findall(r'[^,]+$', header_string)[0] # Retrieve the file path
    print(f"file path: {file_path}")
    header.append(file_path) # add the file path

    # Get the file name
    filename_pattern = '[^/]+$' # Match any 1 or more characters that is not a forward slash till the end of the string
    file_name = re.search(filename_pattern, file_path).group()
    print(f"file name {file_name}")
    handle_files.binary_to_file(file_name, file_data)
    print("file created") """


# So long as there's no KeyboardInterrupt, it will continue to listen
try:
    user = input("")
    while user != KeyboardInterrupt:
        user = input("")
except KeyboardInterrupt:
    print("Exiting...")
    quiting = True

""" import socket

HEADER = 64
PORT = 5050
# HOST = socket.gethostbyname(socket.gethostname())
HOST = "172.20.10.2"
ADDRESS = (HOST, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

intraEndpoint = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def recv_data(endpoint):
    message_length = endpoint.recv(HEADER).decode(FORMAT)

    if message_length:
        message_length = int(message_length)
        message = endpoint.recv(message_length).decode(FORMAT)

    if message == DISCONNECT_MESSAGE:
        endpoint.close()
        return "connection closed"

    return message

def send_data(message):
    message = message.encode(FORMAT)
    msg_length = len(message)
    msg_length = str(msg_length).encode(FORMAT)
    msg_length += b' ' * (HEADER - len(msg_length))
    intraEndpoint.send(msg_length)
    intraEndpoint.send(message)
    # recvd = intraEndpoint.recv(2048).decode(FORMAT)
    # print(recvd)

def get_connection():
    intraEndpoint.connect(ADDRESS)
    print("connected!")

get_connection()
connected = True
while connected:
    print("receiving...")
    received = recv_data(intraEndpoint)
    
    if received:
        print(received)
        send_data("message received!")

    command = str(input("What do you wanna do? "))

    if command == "send":
        message = str(input("What do you wanna send? "))
        send_data(message)

    if command == "end":
        connected = False
        send_data(DISCONNECT_MESSAGE) """

""" 
import socket

HEADER = 64
PORT = 5050 # The port that the client will be connecting to
SERVER = socket.gethostbyname(socket.gethostname()) # The address of the host computer
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT¡"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Client's socket is created
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

send(str(input("What message do you want to send: ")))
send(DISCONNECT_MESSAGE)
 """

""" import socket

HEADERSIZE = 10

intraEndpoint = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
intraEndpoint.connect((socket.gethostname(), 1234))

while True:
    full_msg = ''
    new_msg = True
    while True:
        msg = intraEndpoint.recv(16)
        if new_msg:
            print(f"new message length: {msg[:HEADERSIZE]}")
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg.decode("utf-8")

        if len(full_msg) - HEADERSIZE == msglen:
            print("full msg recvd")
            print(full_msg[HEADERSIZE:])
            new_msg = True
            full_msg = ''

print(full_msg) """