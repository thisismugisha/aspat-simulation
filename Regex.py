import re
import tkinter as tk
from tkinter import filedialog
import bitstring

# Header represented in JSON
ASPAT_header = """{
    "source": "192.168.001.021",
    "destination": "192.168.001.022",
    "packet number": 1,
    "total packets": 1000,
    "hash code": ,
    "data offset": (11, "data"),
    "flags": {
        "rsrvd": 0,
        "cwr": 0,
        "ece": 0,
        "urg": 0,
        "ack": 0,
        "psh": 0,
        "rst": 0,
        "syn": 0,
        "fin": 0,
    },
    "window": 256,
    "checksum": 120EA8A25E5D487BF68B5F7096440019,
    "urgent pointer": ,
    "options": {},
    "data": "THE DATA"
}"""

TCP_header = """{
    "source": "54304" X,
    "destination": "00443" X,
    "sequence number": 0000000001 X,
    "acknowledgement number": 0000000000 X,
    "data offset": (11, "data"),
    "flags": {
        "rsrvd": 0,
        "cwr": 0,
        "ece": 0,
        "urg": 0,
        "ack": 1,
        "psh": 0,
        "rst": 0,
        "syn": 0,
        "fin": 0,
    },
    "window": 00258,
    "checksum": 09842,
    "urgent pointer": ,
    "options": {},
    "data": "THE DATA"
}"""

TCP_header_string = "5430400443000000000100000000006700000100000025809842000000000000000ones and zeroes and junk"

source = '^(?P<src>\d{5})'
destination = '(?P<dst>\d{5})'
sequence = '(?P<seq>\d{10})'
acknowledgement = '(?P<ack>\d{10})'
tcp_data_offset = '(?P<doff>\d{2})'
reserved = '(?P<rsrvd>\d{2})'
flags = '(?P<flg>\d{8})'
window = '(?P<win>\d{5})'
checksum = '(?P<cks>\d{5})'
urgent_pointer = '(?P<urg>\d{5})'
options = '(?P<opt>\d{10})'
data = '(?P<dat>.*)$'

tcp_packet_pattern = source + destination + sequence + acknowledgement + tcp_data_offset + reserved + flags + window + checksum + urgent_pointer + options + data

def binary_padding(*args):
    binary_string = ""
    for arg in args:
        binary, bit_number = arg # Unload the elements to start using them.
        binary = bin(binary).replace("0b", "") # Turn the decimal number into binary and remove 0b from front of the string

        if len(binary) < bit_number:
            binary = ("0" * (bit_number - len(binary))) + binary # Pad the binary string so the whole length is equal to the bit number

        binary_string += binary # Add the binary to the overall binary string
    
    return binary_string

# Hide the root window
root = tk.Tk()
root.withdraw()

# Open the file dialog to select the file
file_path = filedialog.askopenfilename()

# Turn the file to its raw binary representation
bin_data = bitstring.BitArray(filename=file_path).bin

# Open the file and turn its content to hexadecimal value
# file = open(file_path, 'rb').read()
# hex_data = binascii.hexlify(file)

aspat_header_string = "543040044300000000010000001000000000000000060002585430400443" + bin_data

print(aspat_header_string[60])

packet_number = '(?P<pkt_num>\d{10})'
total_packets = '(?P<tot_pkt>\d{10})'
acknowledged_data = '(?P<ack_dat>\d{10})'
DOffset = '(?P<doffset>\d{5})'
crc32 = '(?P<crc32>\d{10})'

aspat_packet_pattern = source + destination + packet_number + total_packets + acknowledged_data + DOffset + window + crc32 + data

def ip_addrs(src, dst):
    src = src[:3] + "." + src[3:6] + "." + src[6:9] + "." + src[9:12]
    dst = dst[:3] + "." + dst[3:6] + "." + dst[6:9] + "." + dst[9:12]
    TCP_head = {
        "Source": src,
        "Destination": dst
    }
    return TCP_head

match = re.search(aspat_packet_pattern, aspat_header_string)

src = 0
dst = 0
pkt_num = 0
tot_pkt = 0
ack_dat = 0
doffset = 0
win = 0
crc32 = 0
dat = 0
if match:

    src = int(match.group('src'))
    dst = int(match.group('dst'))
    pkt_num = int(match.group('pkt_num'))
    tot_pkt = int(match.group('tot_pkt'))
    ack_dat = int(match.group('ack_dat'))
    doffset = int(match.group('doffset'))
    win = int(match.group('win'))
    crc32 = int(match.group('crc32'))
    dat = match.group('dat')

    print(f"Source port:        {binary_padding((src, 16))} {src}")
    print(f"Destination port:   {binary_padding((dst, 16))} {dst}")
    print(f"Packet number:      {binary_padding((pkt_num, 32))} {pkt_num}")
    print(f"Total packets:      {binary_padding((tot_pkt, 32))} {tot_pkt}")
    print(f"Acknowledged data:  {binary_padding((ack_dat, 32))} {ack_dat}")
    print(f"Data Offset:        {binary_padding((doffset, 16))} {doffset}")
    print(f"Window:             {binary_padding((win, 16))} {win}")
    print(f"Checksum:           {binary_padding((crc32, 32))} {crc32}")
    # print(f"Data(binary): {dat}")
else:
    print("No dice!")

aspat_binary_header_string = binary_padding((src, 16), (dst, 16), (pkt_num, 32), (tot_pkt, 32), (ack_dat, 32), (doffset, 16), (win, 16), (crc32, 32))

print(("-"*32) + "\n")
print(aspat_binary_header_string)

"""
                Source Port     |   Destination Port
            1101 0100 0010 0000 | 0000 0001 1011 1011
--------------------------------------------------------------
                        Sequence Number
            0011 0001 1100 1101 1000 0010 1000 0110
-----------------------------------------------------------------
                    Acknowledgement Number
            0100 1010 1101 1110 0010 0001 0010 1100
-----------------------------------------------------------------
DOff | Rsrvd|CWR|ECE|URG|ACK|PSH|RST|SYN|FIN|       Window
0101 | 0000 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0000 0001 0000 0010
-----------------------------------------------------------------
                Checksum        |    Urgent Pointer
            0010 0110 0111 0010 | 0000 0000 0000 0000
-----------------------------------------------------------------

"""