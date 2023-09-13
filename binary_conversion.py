import tkinter as tk
from tkinter import filedialog
import binascii

# Hide the root window
root = tk.Tk()
root.withdraw()

# Open the file dialog to select the file
file_path = filedialog.askopenfilename()

# Print the file content
file = open(file_path, 'rb').read()
hex_data = binascii.hexlify(file)
print(hex_data)