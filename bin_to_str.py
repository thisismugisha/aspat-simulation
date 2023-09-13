import bitstring
import tkinter as tk
from tkinter import filedialog
import re

# Hide the root window
root = tk.Tk()
root.withdraw()

# Open the file dialog to select the file
# file_path = filedialog.askopenfilename()

def file_to_binary_string(file_path):
    with open(file_path, 'rb') as file:
        binary_code = file.read()
        binary_string = ''.join(format(byte, '08b') for byte in binary_code)
    return binary_string


def binary_string_to_file(binary_string, file_path):
    file_extension_pattern = '\..+$'
    file_extension = re.search(file_extension_pattern, file_path).group()
    file = filedialog.asksaveasfilename(defaultextension=file_extension,
                                        filetypes=[
                                            (file_extension, file_extension),
                                            ("Any", ".*"),
                                        ])
    bytes_list = [int(binary_string[i:i+8], 2) for i in range(0, len(binary_string), 8)]
    bytes_arr = bytearray(bytes_list)
    file.write(bytes_arr)
    print("bytes written")

# Usage example
# file_path = 'example.pdf'
# binary_string = file_to_binary_string(file_path)
with open("C:/Users/benja/OneDrive/Desktop/binary_in_text.txt", "r") as binary_in_text:
    file_name = binary_in_text.readline().replace("\n", "")
    binary = binary_in_text.readline()
    binary_string_to_file(binary, file_name.replace(".", "_new."))