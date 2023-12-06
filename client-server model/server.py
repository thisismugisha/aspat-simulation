import socket
import threading
import time
import handle_files
import pickle

PC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = "172.20.10.2"
PORT = 3542
FORMAT = "utf-8"
HEADER = 2048
DISCONNECT = "DISCONNECT"
ADDRESS = (IP, PORT)

PC.bind(ADDRESS)
PC.listen(5)

def recv_data(client_socket):
    message = client_socket.recv(HEADER).decode(FORMAT)
    if message:
        return message
    
def send_data(client_socket, request):
    time.sleep(1)
    print(f"[Sending] {request}")
    client_socket.send(request.encode(FORMAT))
    time.sleep(1)
    print(f"[Sent] {request}\n")

def handle_client(client):
    connected = True
    # client_socket, client_addr = client

    while connected:
        print("[Listening] ready to receive . . .")
        request = handle_files.recv_data(client)
        if request == DISCONNECT or request == None:
            connected = False
            print("\n" + (" " * 15) + ("-" * 15) + (" " * 15))
            print(f"[Disconnecting] closing the connection with {client[1][0]}, request was {request}")
            print(f"[Disconnected]")
            print((" " * 15) + ("-" * 15) + (" " * 15) + "\n\n")
        else:
            try:
                print(f"[Decoded] {request}")
                handle_files.send_data(client, ADDRESS, request)
            except ConnectionResetError:
                connected = False

quiting = False

def listening():
    while not quiting:
        print("[Listening] . . .")
        client = PC.accept()
        print(f"[Connected] new client, {client[1][0]}\n")
        try:
            handle_client(client)
        except ConnectionResetError:
            print("\n" + (" " * 15) + ("-" * 15) + (" " * 15))
            print(f"[Disconnecting] closing the connection with {client[1][0]}")
            print(f"[Disconnected]")
            print((" " * 15) + ("-" * 15) + (" " * 15) + "\n\n")

threading.Thread(target=listening, daemon=True).start()

# So long as there's no KeyboardInterrupt, it will continue to listen
try:
    while True:
        time.sleep(.1)
except KeyboardInterrupt:
    print("Exiting...")
    quiting = True
