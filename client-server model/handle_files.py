import re
import tkinter as tk
from tkinter import filedialog
import bitstring
import binascii
import hashlib
import pickle
import time
import random
import threading
import os
import shutil

def binary_padding(*args):
    """ 
    Takes in an unknown number of arguments. Each argument is a tuple which contains a decimal number in its first index and a second decimal number 
    in its second index denoting the total number of bits that the first decimal number should have once converted to binary. A string containing all of 
    the received arguments is returned.

        Parameters:
            *args (tuple): An unknown number of tuples, where each tuple contains two integers. 

        Returns: 
            binary_string (string): A String containing all converted binary numbers
    """

    binary_string = ""
    print("[Padding] adding 0s to complete a binary word")
    counter = 0
    for arg in args:
        counter += 1
        binary, bit_number = arg # Unload the elements to start using them.
        # binary = bin(binary).replace("0b", "") # Turn the integer into binary and remove 0b from front of the string

        # Sanity check first. Calculate the largest possible integer given the bit word
        max_possible_value = "1" * bit_number
        max_possible_value = int(max_possible_value, 2)

        if binary <= max_possible_value:
            binary = bin(binary).replace("0b", "") # Turn the integer into binary and remove 0b from front of the string
            binary = ("0" * (bit_number - len(binary))) + binary # Pad the binary string so the whole length is equal to the bit number

            # Add the binary to the overall binary string
            binary_string += binary
        else:
            raise ValueError(f"The integer {binary} ({type(binary)}) is bigger than the {bit_number} bit word given. Counter: {counter}")
    
    print("[Results] Returning the binary string")
    return binary_string

def file_to_binary(received_file = None):

    """ 
    Requests a file from the user, converts whatever is received into its binary representation, and returns it as a string. To be called when choosing what data should be sent. 

        Returns:
            tuple (strings): A tuple containing a file name string, a string that contains the binary representation of the file data the user chose, the file data checksum, and the file data hash value
    """

    # Hide the root window
    root = tk.Tk()
    root.wm_attributes('-topmost', 1)
    root.withdraw()

    if received_file not in ["_", "-", ""]:
        # Get the file path and the file name
        file_path = received_file
    else:
        # Open the file dialog to select the file
        print("[File selection] Opening the file dialog to select the file")
        file_path = filedialog.askopenfilename(parent = root)

    # Get the file name
    print("[File name] Getting the file name")
    filename_pattern = '[^/]+$' # Match any 1 or more characters that is not a forward slash till the end of the string
    file_name = re.search(filename_pattern, file_path).group()
    print(f"[File name] File name is \"{file_name}\"")

    # Turn the file to its raw binary representation
    print("[Serializing] Turning the file to its raw binary representation")
    file_data = bitstring.BitArray(filename=file_path).bin

    # Generate a CRC32 checksum
    print("[Error detection] Generating a CRC32 checksum")
    byte_file_data = bytes(file_data, 'utf-8')
    checksum = binascii.crc32(byte_file_data)
    print(f"[Checksum] {checksum}")

    # Generate a SHA256 hash value
    encoded_file_data = file_data.encode('utf-8') # Encode the string
    hash_value = hashlib.sha256(encoded_file_data).hexdigest() # Generate the hash
    
    # Return the binary representation as a string
    print("[Results] Returning the binary representation as a string")
    return ((file_path, file_name), file_data, checksum, hash_value)

def binary_to_file(file_name, file_data, checksum = None, hash_value = None):
    
    """ 
    Turns a string containing binary representation of a file into a file. To be called when data is received

        Parameters:
            file_name (string): a file name , 
            file_data (string): a string that contains the binary representation of a file, 
            checksum (string): the checksum of the file data,
            hash_value (string): a hash value  of the file data.
    """

    # Get a file name and location from user
    file_extension_pattern = '\..[^\.]+$'
    file_extension = re.search(file_extension_pattern, file_name).group()

    suggested_file_name = file_name.replace(file_extension, "")
    save_as_type = file_extension.replace(".", "").upper()

    # Hide the root window
    root = tk.Tk()
    root.wm_attributes('-topmost', 1)
    root.withdraw()

    user_file_name = filedialog.asksaveasfilename(
                                                  initialfile = suggested_file_name,
                                                  defaultextension = file_extension,
                                                  filetypes = [
                                                      (save_as_type, file_extension),
                                                      ("Any", ".*"),
                                                  ]
                                                )
    if user_file_name == None or user_file_name == '':
        return
    
    # Create a new file
    with open(user_file_name, 'wb') as file:

        # Turn bytes to a list of integers
        bytes_list = [int(file_data[i:i+8], 2) for i in range(0, len(file_data), 8)]

        # Turn the list of integers to a bytearray
        bytes_array = bytearray(bytes_list)

        # Write the bytearray to the file
        file.write(bytes_array)

    # Or print the hash and checksum values
    # Generate a CRC32 checksum
    # byte_file_data = bytes(file_data, 'utf-8')
    # checksum = str(binascii.crc32(byte_file_data))
    if checksum:
        print(f"Checksum: {checksum}")

    # Generate a SHA256 hash value
    # encoded_file_data = file_data.encode('utf-8') # Encode the string
    # hash_value = str(hashlib.sha256(encoded_file_data).hexdigest()) # Generate the hash
    if hash_value:
        print(f"Hash value: {hash_value}")

    # Or store the hash value of the file data in a text file
    """ with open("file hash value.txt", 'w') as file:
        file.write(hash_value)
        file.write(bin(hash_value).replace("0b", "")) """
    
def packets_list(file_data, window = None):
    packets = []
    max_packets = []

    # print(f"[File data] Dividing the file data into 8-bit packets")
    while file_data != "":
        first_eight = file_data[:8]
        max_packets.append(first_eight)
        file_data = file_data[8:]

    packet = ""
    # print(f"max_packets: {len(max_packets)}, window: {window}\n")
    if window > 0:
        while max_packets:
            for i in range(window):
                # if max_packets:
                packet += max_packets[0]
                # print(f"max_packets: {len(max_packets)}")
                max_packets.pop(0)
                if len(max_packets) == 0:
                    break
                # print(f"Packet: {packet}, max_packets: {len(max_packets)}")
            
            # print(f"Final packet: {packet}, max_packets: {len(max_packets)}")
            packets.append(packet)
            packet = ""
    else:
        # print(f"[Results] Returning max_packets list: ")
        return max_packets
    
    print("[Results] Returning packets list")
    return packets

def process_header(received_data):
    if received_data == "DISCONNECT":
        return "DISCONNECT"

    elif type(received_data) == tuple:
        return received_data

    elif type(received_data) == str:
        source = '^(?P<src>\d{16})'
        destination = '(?P<dst>\d{16})'
        packet_number = '(?P<pkt_num>\d{32})'
        total_packets = '(?P<tot_pkt>\d{32})'
        acknowledged_data = '(?P<ack_dat>\d{32})'
        dataoffset = '(?P<doffset>\d{16})'
        window = '(?P<win>\d{16})'
        crc32 = '(?P<crc32>\d{32})'
        data = '(?P<dat>.*)$'

        aspat_packet_pattern = source + destination + packet_number + total_packets + acknowledged_data + dataoffset + window + crc32 + data

        match = re.search(aspat_packet_pattern, received_data)
        
        if match:
            source = int(match.group('src'), 2)
            destination = int(match.group('dst'), 2)
            packet_number = int(match.group('pkt_num'), 2)
            total_packets = int(match.group('tot_pkt'), 2)
            acknowledged_data = int(match.group('ack_dat'), 2)
            dataoffset = int(match.group('doffset'), 2)
            window = int(match.group('win'), 2)
            crc32 = int(match.group('crc32'), 2)
            data = match.group('dat')
            
            # return (f"\nsource: {source}, \ndestination: {destination}, \npacket_number: {packet_number}, \ntotal_packets: {total_packets}, \nacknowledged_data: {acknowledged_data}, \ndataoffset: {dataoffset}, \nwindow: {window}, \ncrc32: {crc32}, \ndata: {data}")
            return (source, destination, packet_number, total_packets, acknowledged_data, dataoffset, window, crc32, data)

def recv_data(client, header = None, file_data = None, file_name = None):

    """ 
    Receives data from a socket.
    """

    client_socket, client_addr = client

    try:
        received_data = client_socket.recv(2048)  
        if received_data:
            print(f"[Received] {received_data}")
            received_data = pickle.loads(received_data)
            # print(f"Unpickled: {len(received_data)} {received_data}")
            # print(f"Unpickled: {pickle.loads(received_data)}")

            processed_data = process_header(received_data)
            if processed_data == "DISCONNECT":                
                client_socket.close()
                client_socket.send(pickle.dumps("DISCONNECT"))

            # print(f"Unpickled {received_data}")
            return received_data

            """ if received_data == "DISCONNECT":
                client_socket.close()
                client_socket.send(pickle.dumps("DISCONNECT"))
                return "DISCONNECT"
            
            elif type(received_data) == tuple:
                return received_data
            
            elif type(received_data) == str:
                source = '^(?P<src>\d{16})'
                destination = '(?P<dst>\d{16})'
                packet_number = '(?P<pkt_num>\d{32})'
                total_packets = '(?P<tot_pkt>\d{32})'
                acknowledged_data = '(?P<ack_dat>\d{32})'
                dataoffset = '(?P<doffset>\d{16})'
                window = '(?P<win>\d{16})'
                crc32 = '(?P<crc32>\d{32})'
                data = '(?P<dat>.*)$'

                aspat_packet_pattern = source + destination + packet_number + total_packets + acknowledged_data + dataoffset + window + crc32 + data

                match = re.search(aspat_packet_pattern, received_data)
                
                if match:
                    source = int(match.group('src'))
                    destination = int(match.group('dst'))
                    packet_number = int(match.group('pkt_num'))
                    total_packets = int(match.group('tot_pkt'))
                    acknowledged_data = int(match.group('ack_dat'))
                    dataoffset = int(match.group('doffset'))
                    window = int(match.group('win'))
                    crc32 = int(match.group('crc32'))
                    data = match.group('dat')
                    
                    return (source, destination, packet_number, total_packets, acknowledged_data, dataoffset, window, crc32, data) """
        else:
            print("Nothing has been received") 
    except (ConnectionResetError, ConnectionAbortedError):
        return

def send_data(client, addr, request):

    """ 
    Sends data to a socket.
    """

    client_socket, client_addr = client
    IP, PORT = addr
    source, destination, packet_number, total_packets, acknowledged_data, dataoffset, window, crc32, file_path = request
    # print(f"[Labelled] acknowledged_data: {acknowledged_data}, window: {window}")

    # Getting the file
    print("[File] Getting the file to be sent")
    (file_path, file_name), file_data, checksum, hash_value = file_to_binary(file_path)

    source = PORT # source port
    destination = client_addr[1] # destination port
    dataoffset = 192
    crc32 = checksum

    # Prepare the packets
    print("[Packets] preparing to get packets")
    packets = packets_list(file_data, window=window)
    total_packets = len(packets)
    print(f"[Packets] packets length: {total_packets}")

    header = [source, destination, packet_number, total_packets, acknowledged_data, dataoffset, window, crc32, file_path]

    print(f"\n[ASPAT header] created the header: \nsource: {source}, destination: {destination}, packet_number: {packet_number}, total_packets: {total_packets}, acknowledged_data: {acknowledged_data}, dataoffset: {dataoffset}, window: {window}, crc32: {crc32}, file_path: {file_path}")
        
    # print(f"    source: {source}")
    # print(f"    destination: {destination}")
    # print(f"    packet_number: {packet_number}")
    # print(f"    total_packets: {total_packets}")
    # print(f"    acknowledged_data: {acknowledged_data}")
    # print(f"    dataoffset: {dataoffset}")
    # print(f"    window: {window}")
    # print(f"    crc32: {crc32}")
    # print(f"    file_name: {file_path}")

    # Send the file name
    message = pickle.dumps(header)
    # print(f"[ASPAT header] pickled the header")
    client_socket.send(message)
    print(f"[ASPAT header] pickled and sent the header: {len(message)} {message}")

    print("-" * 50)

    if acknowledged_data == 0:
        # For unreliable data transfer
        print("\n[Transfer type] Data transfer is unreliable\n")
        for packet in range(packet_number, total_packets):
            header = [source, destination, packet, total_packets, acknowledged_data, dataoffset, window, crc32, file_path]
            print(f"header: {header}")
            message = header.copy()
            message.append(packets[packet])
            print(f"[Message] Combined the header with the data: {message}")

            message = pickle.dumps(message)
            print(f"[Encode] Encoded the message to be sent: {message}")

            try:
                client_socket.send(message)
                print(f"[Sent] Sent {message}")
            except (KeyboardInterrupt, ConnectionResetError, ConnectionAbortedError):
                return            
            
            print(f"[Packet count] Sent {(packet + 1)} of {total_packets}\n\n")
            time.sleep(random.randint(1, 2))
    else:
        # For reliable data transfer
        print("\n[Transfer type] Data transfer is reliable\n")
        for packet in range(packet_number, total_packets):
            header = [source, destination, packet, total_packets, acknowledged_data, dataoffset, window, crc32, file_path]
            print(f"header: {header}")
            message = header.copy()
            message.append(packets[packet])
            print(f"[Message] Combined the header with the data: {message}")

            message = pickle.dumps(message)
            print(f"[Encode] Encoded the message to be sent: {message}")

            try:
                client_socket.send(message)
                print(f"[Sent] Sent {message}")
            except (KeyboardInterrupt, ConnectionResetError, ConnectionAbortedError):
                return
            
            print(f"[Packet count] Sent {(packet + 1)} of {total_packets}\n\n")
            
            print("\n" + (" " * 5) + ("-" * 10) + (" " * 5))
            try:
                header = client_socket.recv(2048)
                header = pickle.loads(header)
                source, destination, packet, total_packets, acknowledged_data, dataoffset, window, crc32, file_path = header
                print(f"[Acknowledgement] source: {source}, destination: {destination}, packet: {packet}, total_packets: {total_packets}, acknowledged_data: {acknowledged_data}, dataoffset: {dataoffset}, window: {window}, crc32: {crc32}, file_path: {file_path}")
                print((" " * 5) + ("-" * 10) + (" " * 5) + "\n")
            except (KeyboardInterrupt, ConnectionResetError, ConnectionAbortedError):
                return
            
            time.sleep(random.randint(1, 2))
