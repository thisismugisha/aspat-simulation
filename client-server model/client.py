import socket
import handle_files
import pickle
import os
import shutil
import threading
import re
import time

# Variables required for file manipulation
pattern = r',?([0-9]+),?'
temp_dir = "./temp_dir/"
temp_header_file = temp_dir + "temp_header_file.txt"
temp_binary_file = temp_dir + "temp_binary_file.txt"
delete_order = temp_dir + "delete_order.txt"

# Variables required for socket connection
PC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = "172.20.10.2"
PORT = 3542
FORMAT = "utf-8"
HEADER = 2048
DISCONNECT = "DISCONNECT"

quiting = False

def rm_temp_dir(temp_dir):
    deleted = False
    does_exist = os.path.isfile(delete_order)
    while not does_exist:
        does_exist = os.path.isfile(delete_order)
    
    # print(f"The delete order does exist: {does_exist}")

    with open(delete_order, "r") as delete_file:
        while not deleted:
            delete_file.seek(0)
            delete = int(delete_file.read())
            print(f"\nDelete order: {delete}")
            time.sleep(0.5)
            if delete == 1:
                deleted = True
                # return deleted
    print("deleting the temporary folder")
    shutil.rmtree(temp_dir)
    print("deleted")

""" def previous_transfer(header_file, binary_file):
    print("Going to the beginning of the binary file")
    binary_file.seek(0) # Go to the beginning of the file
    file_data = binary_file.read() # Read from the beginning
    print(f"file data: {file_data}")
    
    # print("Reading the header file")
    # header_string = header_file.read() # Read what's in it
    # print(f"header string: {header_string}")
    # header = [int(i) for i in re.findall(pattern, header_string)] # turn string back to a list (except the file name)

    print("[Header] reading the header file")
    header_string = header_file.read() # Read what's in it
    print(f"header string: {header_string}")
    header = [int(i) for i in re.findall(pattern, header_string)] # turn string back to a list (except the file name)
    
    file_path = re.findall(r'[^,]+$', header_string)[0] # Retrieve the file path
    print(f"file path: {file_path}")
    header.append(file_path) # add the file path
    print(f"header: {header}")

    if (header[2] + 1) == header[3]:
        # Get the file name
        filename_pattern = '[^/]+$' # Match any 1 or more characters that is not a forward slash till the end of the string
        file_name = re.search(filename_pattern, file_path).group()
        print(f"file name {file_name}")
        handle_files.binary_to_file(file_name, file_data)
        print("file created")

        delete = input("Delete the temporary file? [0] for no, [1] for yes")
        if delete == 1:
            rm_temp_dir(temp_dir)
        return True
    return header """

def start():
    os.makedirs(os.path.dirname(temp_dir), exist_ok=True) # create/open temporary directory
    print("[Temporary directory] it exists now")

    # def open_temp_files(exists):
    exists = os.path.isfile(temp_header_file) and os.path.isfile(temp_binary_file) # check if there are temporary header and binary files

    if exists:
        # Both temporary files are opened
        with open(temp_header_file, "r+") as header_file, open(temp_binary_file, "a+") as binary_file, open(delete_order, "w") as delete_file:            
            
            # --------------------------------------- header file ---------------------------------------
            # Check the previous progress
            print("[Data] reading the binary file")
            binary_file.seek(0) # Go to the beginning of the file
            file_data = binary_file.read() # Read from the beginning
            print(f"file data: {file_data}")

            print("[Header] reading the header file")
            header_file.seek(0) # Go to the beginning of the file
            header_string = header_file.read() # Read what's in it
            print(f"header string: {header_string}")
            header = [int(i) for i in re.findall(pattern, header_string)] # turn string back to a list (except the file name)
            
            file_path = re.findall(r'[^,]+$', header_string)[0] # Retrieve the file path
            print(f"file path: {file_path}")
            header.append(file_path) # add the file path
            print(f"header: {header}")

            if (header[2] + 1) == header[3]:
                # Get the file name
                filename_pattern = '[^/]+$' # Match any 1 or more characters that is not a forward slash till the end of the string
                file_name = re.search(filename_pattern, file_path).group()
                print(f"file name {file_name}")
                handle_files.binary_to_file(file_name, file_data)
                print("file created")
                delete_file.write("1")
                print("Exiting...")
                return True
            
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
                                source, destination, packet_number, total_packets, acknowledged_data, dataoffset, window, crc32, file_path = received # Unbox all the variables
                                print(f"\n[ASPAT header] created the header: \nsource: {source}, destination: {destination}, packet_number: {packet_number}, total_packets: {total_packets}, acknowledged_data: {acknowledged_data}, dataoffset: {dataoffset}, window: {window}, crc32: {crc32}, file_path: {file_path}")
                                reliable = (acknowledged_data == 1)
                                for packet in range(packet_number, total_packets):
                                    received = PC.recv(2048)
                                    received = pickle.loads(received)
                                    source, destination, packet_number, total_packets, acknowledged_data, dataoffset, window, crc32, file_path, data = received # Unbox all the variables
                                    if reliable:
                                        # Make sure the old header content are not deleted
                                        old_header = ""
                                        try:
                                            header_file.seek(0)
                                            old_header = header_file.read()
                                            # print(f"Old header: {len(old_header)}")
                                        except KeyboardInterrupt:
                                            header_file.write(old_header)
                                            
                                        # Add to the binary file
                                        binary_file.seek(0, 2) # Go to the end of the file
                                        binary_file.write(data) # Append new content at the end of the file

                                        binary_file.seek(0) # Go to the beginning of the file
                                        file_data = binary_file.read() # Read from the beginning
                                        acknowledged_data = len(file_data)
                                        
                                        # Update the header file
                                        header_list = [source, destination, packet_number, total_packets, acknowledged_data, dataoffset, window, crc32, file_path]
                                        print("Created the header list")
                                        header = ",".join(str(s) for s in header_list)
                                        print("Turned the list to a string")
                                        
                                        # Make sure the old header content are not deleted
                                        try:
                                            header_file.seek(0)
                                            old_header = header_file.read()
                                            # print(f"Old header: {len(old_header)}")
                                        except KeyboardInterrupt:
                                            header_file.write(old_header)

                                        header_file.truncate(0) # Delete what was in it
                                        print("Deleted what was in it")
                                        header_file.seek(0) # Go to the beginning of the file
                                        print("Put cursor at the beginning of the file")
                                        header_file.write(header) # Write new content
                                        print("Wrote the new header")
                                        
                                        # Make sure the old header content are not deleted
                                        try:
                                            header_file.seek(0)
                                            old_header = header_file.read()
                                            # print(f"\nNew header: {len(old_header)}\n")
                                        except KeyboardInterrupt:
                                            header_file.write(old_header)

                                        # Send the header
                                        PC.send(pickle.dumps(header_list)) # Pickle and send the header to acknowledge the reception of the packet

                                        print(f"[Packet count] Received {(packet + 1)} of {total_packets}\n\n")
                                        print(header, data)
                                    else:
                                        # Make sure the old header content are not deleted
                                        old_header = ""
                                        try:
                                            header_file.seek(0)
                                            old_header = header_file.read()
                                            # print(f"Old header: {len(old_header)}")
                                        except KeyboardInterrupt:
                                            header_file.write(old_header)
                                            
                                        # Add to the binary file
                                        binary_file.seek(0, 2) # Go to the end of the file
                                        binary_file.write(data) # Append new content at the end of the file
                                        
                                        # Update the header file
                                        header_list = [source, destination, packet_number, total_packets, acknowledged_data, dataoffset, window, crc32, file_path]
                                        print("Created the header list")
                                        header = ",".join(str(s) for s in header_list)
                                        print("Turned the list to a string")
                                        
                                        # Make sure the old header content are not deleted
                                        try:
                                            header_file.seek(0)
                                            old_header = header_file.read()
                                            # print(f"Old header: {len(old_header)}")
                                        except KeyboardInterrupt:
                                            header_file.write(old_header)

                                        header_file.truncate(0) # Delete what was in it
                                        print("Deleted what was in it")
                                        header_file.seek(0) # Go to the beginning of the file
                                        print("Put cursor at the beginning of the file")
                                        header_file.write(header) # Write new content
                                        print("Wrote the new header")
                                        
                                        # Make sure the old header content are not deleted
                                        try:
                                            header_file.seek(0)
                                            old_header = header_file.read()
                                            # print(f"\nNew header: {len(old_header)}\n")
                                        except KeyboardInterrupt:
                                            header_file.write(old_header)

                                        print(f"[Packet count] Received {(packet + 1)} of {total_packets}\n\n")
                                        print(header, data)
                                        
                        # Check the previous progress
                        print("[Data] reading the binary file")
                        binary_file.seek(0) # Go to the beginning of the file
                        file_data = binary_file.read() # Read from the beginning
                        print(f"file data: {file_data}")

                        print("[Header] reading the header file")
                        header_file.seek(0) # Go to the beginning of the file
                        header_string = header_file.read() # Read what's in it
                        print(f"header string: {header_string}")
                        header = [int(i) for i in re.findall(pattern, header_string)] # turn string back to a list (except the file name)
                        
                        file_path = re.findall(r'[^,]+$', header_string)[0] # Retrieve the file path
                        print(f"file path: {file_path}")
                        header.append(file_path) # add the file path
                        print(f"header: {header}")

                        if (header[2] + 1) == header[3]:
                            # Get the file name
                            filename_pattern = '[^/]+$' # Match any 1 or more characters that is not a forward slash till the end of the string
                            file_name = re.search(filename_pattern, file_path).group()
                            print(f"file name {file_name}")
                            handle_files.binary_to_file(file_name, file_data)
                            print("file created")
                            delete_file.write("1")
                            print("Exiting...")
                            return True

                    except (KeyboardInterrupt, ConnectionResetError):
                        print(f"[Disconnected] connection closed\n")
                        print("Exiting...")
                        connected = False
            except ConnectionRefusedError:
                print("\nCouldn\'t connect. Exiting\n")
                return

            # --------------------------------------- data file ---------------------------------------
            """ print("\nreading the binary file")
            binary_file.seek(0) # Go to the beginning of the file
            file_data = binary_file.read() # Read from the beginning
            print(f"binary file: {file_data}\n")

            binary_file.seek(0, 2) # Go to the end of the file
            binary_file.write(str(input("Write what you wanna add to the binary file: "))) # Append new content at the end of the file
            print("added to the binary")
            binary_file.seek(0) # Go to the beginning of the file
            file_data = binary_file.read() # Read from the beginning
            print(f"new binary file: {file_data}\n") """
    else:        
        with open(temp_header_file, "w") as header_file, open(temp_binary_file, "x"):
            header_ = [0, 0, 0, 0, 0, 192, 3, 0, "_"]
            header = ",".join(str(s) for s in header_) # turn to a string
            header_file.write(header)
            print(f"[Temp files] Created the temporary files {header}")
        
        start()

threading.Thread(target=start, daemon=True).start()

try:
    while True:
        time.sleep(.1)
except KeyboardInterrupt:
    rm_temp_dir(temp_dir)
    print("Quiting...")
    quiting = True
