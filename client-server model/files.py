import re
import handle_files
import pickle
import os
import shutil
from pathlib import Path

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
            source = int(match.group('src'))
            destination = int(match.group('dst'))
            packet_number = int(match.group('pkt_num'))
            total_packets = int(match.group('tot_pkt'))
            acknowledged_data = int(match.group('ack_dat'))
            dataoffset = int(match.group('doffset'))
            window = int(match.group('win'))
            crc32 = int(match.group('crc32'))
            data = match.group('dat')
            
            # return (f"\nsource: {source}, \ndestination: {destination}, \npacket_number: {packet_number}, \ntotal_packets: {total_packets}, \nacknowledged_data: {acknowledged_data}, \ndataoffset: {dataoffset}, \nwindow: {window}, \ncrc32: {crc32}, \ndata: {data}")
            return (source, destination, packet_number, total_packets, acknowledged_data, dataoffset, window, crc32, data)

cutoff_16 = 65535
cutoff_32 = 4294967295

""" source = 0
while True:
    try:
        source = int(input(f"source (num): "))
        if source <= cutoff_16:
            break
        else:
            print(f"{source} is bigger than 65535.")
    except ValueError:
        print(f"Source must be an int.")
        continue

destination = 0
while True:
    try:
        destination = int(input(f"destination (num): "))
        if destination <= cutoff_16:
            break
        else:
            print(f"{destination} is bigger than 65535.")
    except ValueError:
        print(f"Destination must be an int.")
        continue

packet_number = 0
while True:
    try:
        packet_number = int(input(f"packet_number (num): "))
        if packet_number <= cutoff_32:
            break
        else:
            print(f"{packet_number} is bigger than {cutoff_32}.")
    except ValueError:
        print(f"packet_number must be an int.")
        continue

total_packets = 0
while True:
    try:
        total_packets = int(input(f"total_packets (num): "))
        if total_packets <= cutoff_32:
            break
        else:
            print(f"{total_packets} is bigger than {cutoff_32}.")
    except ValueError:
        print(f"total_packets must be an int.")
        continue

acknowledged_data = 0
while True:
    try:
        acknowledged_data = int(input(f"acknowledged_data (num): "))
        if acknowledged_data <= cutoff_32:
            break
        else:
            print(f"{acknowledged_data} is bigger than {cutoff_32}.")
    except ValueError:
        print(f"acknowledged_data must be an int.")
        continue

dataoffset = 0
while True:
    try:
        dataoffset = int(input(f"dataoffset (num): "))
        if dataoffset <= cutoff_16:
            break
        else:
            print(f"{dataoffset} is bigger than {cutoff_16}.")
    except ValueError:
        print(f"dataoffset must be an int.")
        continue

window = 0
while True:
    try:
        window = int(input(f"window (num): "))
        if window <= cutoff_16:
            break
        else:
            print(f"{window} is bigger than {cutoff_16}.")
    except ValueError:
        print(f"window must be an int.")
        continue

crc32 = 0
while True:
    try:
        crc32 = int(input(f"crc32 (num): "))
        if crc32 <= cutoff_32:
            break
        else:
            print(f"{crc32} is bigger than {cutoff_32}.")
    except ValueError:
        print(f"crc32 must be an int.")
        continue """

pattern = r',?([0-9]+),?'
data = "jdffd" # str(input(f"data (num): "))
# aspat_binary_header_string = handle_files.binary_padding((65535, 16), (65535, 16), (65535, 32), (65535, 32), (65535, 32), (65535, 16), (65535, 16), (65535, 32))
aspat_binary_header_string = [65535, 65535, 65535, 65535, 65535, 65535, 65535, 65535]

message = aspat_binary_header_string.copy()
message.append(data)

temp_dir = "./temp_dir/"
temp_header_file = temp_dir + "temp_header_file.txt"
temp_binary_file = temp_dir + "temp_binary_file.txt"

os.makedirs(os.path.dirname(temp_dir), exist_ok=True)

def open_temp_files(exists):
    if exists:
        with open(temp_header_file, "r+") as header_file, open(temp_binary_file, "a+") as binary_file:
            # --------------------------------------- header file ---------------------------------------
            print("reading the header file")
            header_string = header_file.read() # Read what's in it
            print(f"\n{header_string}, {type(header_string)}\n")
            header = [int(i) for i in re.findall(pattern, header_string)] # list_string_converter(header_string, toList=True) # turn back to a list
            print(f"header before: {header}\n")
            source, destination, packet_number, total_packets, acknowledged_data, dataoffset, window, crc32 = header # Unbox all the variables
            
            packet_number = 0
            binary_header_list = [source, destination, packet_number, total_packets, acknowledged_data, dataoffset, window, crc32]
            binary_header = ",".join(str(s) for s in binary_header_list) # turn to a string
            header_file.truncate(0) # Delete what was in it
            header_file.write(binary_header) # Write new content
            header_file.seek(0) # Go to the beginning of the file
            header_string = header_file.read() # Read from the beginning
            header = [int(i) for i in re.findall(pattern, header_string)] # list_string_converter(header_string, toList=True) # turn back to a list
            print(f"header after: {header}\n")

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
        
        with open(temp_header_file, "w") as header_file, open(temp_binary_file, "w") as binary_file:
            header = ",".join(str(s) for s in aspat_binary_header_string) # turn to a string
            header_file.write(header)
            print(f"written the header: {header}")

            binary_file.write(data)
            print("written the binary")

open_temp_files(os.path.isfile(temp_header_file) and os.path.isfile(temp_binary_file))
