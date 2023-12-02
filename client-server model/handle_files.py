import re
import tkinter as tk
from tkinter import filedialog
import bitstring
import binascii
import hashlib
import pickle
import time
import random

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
    for arg in args:
        binary, bit_number = arg # Unload the elements to start using them.
        # print(f"int: {binary}, binary: {bin(binary).replace('0b', '')}, type: {type(bin(binary).replace('0b', ''))}")
        binary = bin(binary).replace("0b", "") # Turn the decimal number into binary and remove 0b from front of the string


        if len(binary) < bit_number:
            binary = ("0" * (bit_number - len(binary))) + binary # Pad the binary string so the whole length is equal to the bit number

        # Add the binary to the overall binary string; as long as that binary is a multiple of 8
        binary_string += binary if len(binary) % 8 == 0 else print(f"{binary} is not a multiple of 8") 
    
    print("[Results] Returning the binary string")
    return binary_string

def file_to_binary():

    """ 
    Requests a file from the user, converts whatever is received into its binary representation, and returns it as a string. To be called when choosing what data should be sent. 

        Returns:
            tuple (strings): A tuple containing a file name string, a string that contains the binary representation of the file data the user chose, the file data checksum, and the file data hash value
    """

    # Hide the root window
    root = tk.Tk()
    root.withdraw()

    # Open the file dialog to select the file
    print("[File selection] Opening the file dialog to select the file")
    file_path = filedialog.askopenfilename()

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
    checksum = str(binascii.crc32(byte_file_data))
    print(f"[Checksum] {checksum}")

    # Generate a SHA256 hash value
    encoded_file_data = file_data.encode('utf-8') # Encode the string
    hash_value = str(hashlib.sha256(encoded_file_data).hexdigest()) # Generate the hash
    
    # Return the binary representation as a string
    print("[Results] Returning the binary representation as a string")
    return (file_name, file_data, checksum, hash_value)

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

    print(f"[File data] Dividing the file data into 8-bit packets")
    while file_data != "":
        first_eight = file_data[:8]
        max_packets.append(first_eight)
        file_data = file_data[8:]

    packet = ""
    print(f"max_packets: {len(max_packets)}, window: {window}\n")
    if window > 0:
        while max_packets:
            for i in range(window):
                # if max_packets:
                packet += max_packets[0]
                print(f"max_packets: {len(max_packets)}")
                max_packets.pop(0)
                if len(max_packets) == 0:
                    break
                # print(f"Packet: {packet}, max_packets: {len(max_packets)}")
            
            # print(f"Final packet: {packet}, max_packets: {len(max_packets)}")
            packets.append(packet)
            packet = ""
    else:
        print("[Results] Returning max_packets list")
        return max_packets
    
    print("[Results] Returning packets list")
    return packets

def recv_data(client, header = None, file_data = None, file_name = None):

    """ 
    Receives data from a socket.
    """

    client_socket = client
    received_data = ""
    if header:
        received_data = client_socket.recv(header)
    else:
        received_data = client_socket.recv(64)

    print(f"[Received] {received_data}")
    received_data = pickle.loads(received_data)

    if received_data == "DISCONNECT":
        return "DISCONNECT"
    
    # if received_data == type(tuple):
    #     return received_data

    # Regex patterns to find or assemble necessary information of a string.
    """ source = '^(?P<src>\d{16})'
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

        # binary_to_file(file_name, file_data, checksum = crc32)
        # print(f"A file called {file_name} has been created")

        # if file_name:
        #     # Data is a file name
        #     return (packet_number, total_packets, acknowledged_data, window, data)

        # else:
        #     # Data is a file
        #     binary_to_file(file_name, file_data, checksum = crc32)
        return (packet_number, total_packets, acknowledged_data, window) """

        # return True
    return received_data

def send_data(client, addr, request):

    """ 
    Sends data to a socket.
    """

    client_socket, client_addr = client
    IP, PORT = addr
    acknowledged_data, window = request
    print(f"[Labelled] acknowledged_data: {acknowledged_data}, window: {window}")

    # Getting the file
    print("[Fetching] Getting the file to be sent")
    file_name, file_data, checksum, hash_value = file_to_binary()

    # Send the file name
    message = pickle.dumps(file_name)
    print(f"[Encode] pickled the file name: {file_name}")
    client_socket.send(message)
    print(f"[Send] sent the file name")
    
    data_length = len(file_data)
    max_packets = int(data_length / 8) if data_length % 8 == 0 else data_length / 8

    # Regex patterns to find or assemble necessary information of a string.
    # source = '^(?P<src>\d{16})'
    # destination = '(?P<dst>\d{16})'
    # packet_number = '(?P<pkt_num>\d{32})'
    # total_packets = '(?P<tot_pkt>\d{32})'
    # acknowledged_data = '(?P<ack_dat>\d{32})'
    # dataoffset = '(?P<doffset>\d{16})'
    # window = '(?P<win>\d{16})'
    # crc32 = '(?P<crc32>\d{32})'
    # data = '(?P<dat>.*)$'

    src = int(PORT) # source port
    dst = int(client_addr[1]) # destination port
    ack_dat = int(acknowledged_data)
    doffset = int(192)
    win = int(window) if window <= 65535 else 0
    crc32 = int(checksum)
    # data = "".join(format(ord(character), 'b') for character in file_name)

    # Prepare the packets
    print("[Packets] preparing to get packets")
    packets = packets_list(file_data, window=win)
    print(f"[Packets] Got packets: {len(packets)}")
    pkt_num = int(1)
    tot_pkt = int(len(packets))

    aspat_binary_header_string = binary_padding((src, 16), (dst, 16), (pkt_num, 32), (tot_pkt, 32), (ack_dat, 32), (doffset, 16), (win, 16), (crc32, 32))
    print(f"\n[ASPAT header] Created the header: {aspat_binary_header_string}")
    # print(len(aspat_binary_header_string)/8)

    # Prepare the packets
    # packets = packets_list(file_data, window=window)

    if acknowledged_data == 0:
        # For unreliable data transfer
        print("\n[Transfer type] Data transfer is unreliable\n")
        for packet in range (pkt_num, tot_pkt):
            message = aspat_binary_header_string + packets[packet]
            print("[Message] Combined the header with the data")

            message = pickle.dumps(message)
            print("[Encode] Encoded the message to be sent")

            client_socket.send(message)
            print("[Sent] Sent the message")
            aspat_binary_header_string = binary_padding((src, 16), (dst, 16), (packet, 32), (tot_pkt, 32), (0, 32), (doffset, 16), (win, 16), (crc32, 32))
            print(f"[Packet count] Sent {packet} of {tot_pkt}\n\n")
            time.sleep(random.randint(1, 3))
    else:
        # For reliable data transfer
        print("\n[Transfer type] Data transfer is reliable\n")
        for packet in range (pkt_num, tot_pkt):
            message = aspat_binary_header_string + packets[packet]
            print("[Message] Combined the header with the data")

            message = pickle.dumps(message)
            print("[Encode] Encoded the message to be sent")

            client_socket.send(message)
            print("[Sent] Sent the message")
            print(f"[Packet count] Sent {packet} of {tot_pkt}")
            time.sleep(random.randint(1, 3))
            
            print("-" *50)
            ack_dat = client_socket.recv(64) # Receive the ack
            print("[Acknowledgement] Received the ack")

            ack_dat = pickle.loads(ack_dat)
            print("[Decode] Decoded the ack")

            aspat_binary_header_string = binary_padding((src, 16), (dst, 16), (packet, 32), (tot_pkt, 32), (ack_dat, 32), (doffset, 16), (win, 16), (crc32, 32))

# def packet_list(file_data):
#     length = len(file_data)
#     packets = int(length / 8) if length % 8 == 0 else length / 8

# Regex patterns to find or assemble necessary information of a string.
# source = '^(?P<src>\d{16})'
# destination = '(?P<dst>\d{16})'
# packet_number = '(?P<pkt_num>\d{32})'
# total_packets = '(?P<tot_pkt>\d{32})'
# acknowledged_data = '(?P<ack_dat>\d{32})'
# doffset = '(?P<doffset>\d{16})'
# window = '(?P<win>\d{16})'
# crc32 = '(?P<crc32>\d{32})'
# data = '(?P<dat>.*)$'

# src = 0
# dst = 0
# pkt_num = 0
# tot_pkt = 0
# ack_dat = 0
# doffset = 0
# win = 0
# crc32 = 0

# aspat_packet_pattern = source + destination + packet_number + total_packets + acknowledged_data + doffset + window + crc32 + data
# bin_data = get_data_in_binary()
# aspat_binary_header_string = binary_padding((src, 16), (dst, 16), (pkt_num, 32), (tot_pkt, 32), (ack_dat, 32), (doffset, 16), (win, 16), (crc32, 32)) + bin_data