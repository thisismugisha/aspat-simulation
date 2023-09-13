source = 54304
destination = 443
sequence_number = 1
acknowledgement_number = 0

def binary_padding(binary, bit_number):
    if len(binary) < bit_number:
        binary = ("0" * (bit_number - len(binary))) + binary
    
    return binary

bin_src = binary_padding(bin(source).replace("0b", ""), 16) # 16 bits
bin_dst = binary_padding(bin(destination).replace("0b", ""), 16) # 16 bits
bin_seq = binary_padding(bin(sequence_number).replace("0b", ""), 32) # 32 bits
bin_ack = binary_padding(bin(acknowledgement_number).replace("0b", ""), 32) # 32 bits

print(f"source in binary: {bin_src} ")
print(f"destination in binary: {bin_dst} ")
print(f"sequence_number in binary: {bin_seq} ")
print(f"acknowledgement_number in binary: {bin_ack} ")

print(("-"*32) + "\n")

print(f"source in decimal: {int(bin_src, 2)} ")
print(f"destination in decimal: {int(bin_dst, 2)} ")
print(f"sequence_number in decimal: {int(bin_seq, 2)} ")
print(f"acknowledgement_number in decimal: {int(bin_ack, 2)} ")

