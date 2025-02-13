import re
import tkinter as tk
from tkinter import filedialog
import bitstring
import binascii
import hashlib

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
    for arg in args:
        binary, bit_number = arg # Unload the elements to start using them.
        binary = bin(binary).replace("0b", "") # Turn the decimal number into binary and remove 0b from front of the string

        if len(binary) < bit_number:
            binary = ("0" * (bit_number - len(binary))) + binary # Pad the binary string so the whole length is equal to the bit number

        # Add the binary to the overall binary string; as long as that binary is a multiple of 8
        binary_string += binary if binary % 8 == 0 else print(f"{binary} is not a multiple of 8") 
    
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
    file_path = filedialog.askopenfilename()

    # Get the file name
    filename_pattern = '[^/]+$' # Match any 1 or more characters that is not a forward slash till the end of the string
    file_name = re.search(filename_pattern, file_path).group()

    # Turn the file to its raw binary representation
    file_data = bitstring.BitArray(filename=file_path).bin

    # Generate a CRC32 checksum
    byte_file_data = bytes(file_data, 'utf-8')
    checksum = str(binascii.crc32(byte_file_data))

    # Generate a SHA256 hash value
    encoded_file_data = file_data.encode('utf-8') # Encode the string
    hash_value = str(hashlib.sha256(encoded_file_data).hexdigest()) # Generate the hash
    
    # Return the binary representation as a string
    return (file_name, file_data, checksum, hash_value)

def binary_to_file(file_name, file_data):
    
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
    """ with open(user_file_name, 'wb') as file:

        # Turn bytes to a list of integers
        bytes_list = [int(file_data[i:i+8], 2) for i in range(0, len(file_data), 8)]

        # Turn the list of integers to a bytearray
        bytes_array = bytearray(bytes_list)

        # Write the bytearray to the file
        file.write(bytes_array) """

    # Or print the hash and checksum values
    # Generate a CRC32 checksum
    byte_file_data = bytes(file_data, 'utf-8')
    checksum = str(binascii.crc32(byte_file_data))
    print(f"Checksum: {checksum}")

    # Generate a SHA256 hash value
    encoded_file_data = file_data.encode('utf-8') # Encode the string
    hash_value = str(hashlib.sha256(encoded_file_data).hexdigest()) # Generate the hash
    print(f"Hash value: {hash_value}")

    # Or store the hash value of the file data in a text file
    """ with open("file hash value.txt", 'w') as file:
        file.write(hash_value)
        file.write(bin(hash_value).replace("0b", "")) """

def recv_data():

    """ 
    Receives data from a socket.
    """

    pass

def send_data():

    """ 
    Sends data to a socket.
    """

    file_name, file_data, checksum, hash_value = file_to_binary()

# Regex patterns to find or assemble necessary information of a string.
source = '^(?P<src>\d{16})'
destination = '(?P<dst>\d{16})'
packet_number = '(?P<pkt_num>\d{32})'
total_packets = '(?P<tot_pkt>\d{32})'
acknowledged_data = '(?P<ack_dat>\d{32})'
doffset = '(?P<doffset>\d{16})'
window = '(?P<win>\d{16})'
crc32 = '(?P<crc32>\d{32})'
data = '(?P<dat>.*)$'


src = 0
dst = 0
pkt_num = 0
tot_pkt = 0
ack_dat = 0
doffset = 0
win = 0
crc32 = 0

# aspat_packet_pattern = source + destination + packet_number + total_packets + acknowledged_data + doffset + window + crc32 + data
# bin_data = get_data_in_binary()
# aspat_binary_header_string = binary_padding((src, 16), (dst, 16), (pkt_num, 32), (tot_pkt, 32), (ack_dat, 32), (doffset, 16), (win, 16), (crc32, 32)) + bin_data