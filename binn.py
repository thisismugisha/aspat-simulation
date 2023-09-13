import bitstring
import tkinter as tk
from tkinter import filedialog
import re

def file_to_binary():
    # Hide the root window
    root = tk.Tk()
    root.withdraw()

    # Open the file dialog to select the file
    file_path = filedialog.askopenfilename()

    # Get the file name
    filename_pattern = '[^/]+$' # Match any 1 or more characters that is not a forward slash till the end of the string
    file_name = re.search(filename_pattern, file_path).group()

    # Turn the file to its raw binary representation
    binary_as_string = bitstring.BitArray(filename=file_path).bin
    
    # Return the binary representation as a string
    return (file_name, binary_as_string)

def binary_to_file(file_name, binary_as_string):
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
        bytes_list = [int(binary_as_string[i:i+8], 2) for i in range(0, len(binary_as_string), 8)]

        # Turn the list of integers to a bytearray
        bytes_arr = bytearray(bytes_list)

        # Write the bytearray to the file
        file.write(bytes_arr)

file_name, binary_as_string = file_to_binary()
binary_to_file(file_name, binary_as_string)

with open("C:/Users/benja/OneDrive/Desktop/binary_in_text.txt", "w") as binary_in_text:
    print(f"[writing] the file name: {file_name}")
    binary_in_text.write(file_name + "\n")
    print("[writing] the raw binary...")
    binary_in_text.write(binary_as_string)

b = len(binary_as_string)
B = b/8
KB = B/1000
MB = KB/1000
print(f"[written] {b} bits | {B} bytes | {KB} KB | {MB} MB")