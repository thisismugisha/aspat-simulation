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

""" def packets_list(file_data, window = None):
    packets = []
    max_packets = []

    while file_data != "":
        first_eight = file_data[:8]
        max_packets.append(first_eight)
        file_data = file_data[8:]

    packet = ""
    if window:
        while max_packets:
            for i in range(window):
                packet += max_packets[0]
                max_packets.pop(0)
            packets.append(packet)
            packet = ""
    else:
        return max_packets

    return packets """

def handle_client(client):

    packet_number = 0
    total_packets = 0
    acknowledged_data = 0
    window = 0
    data = 0

    connected = True
    client_socket, client_addr = client
    # message = f"Welcome to the server, {client_addr}! What window would you prefer. "
    # message = pickle.dumps(message)
    # client_socket.send(message)
    while connected:
        # request = recv_data(client_socket)
        request = handle_files.recv_data(client_socket)
        print(f"[Decoded] {request}")
        if request == DISCONNECT:
            connected = False
            print(f"[Disconnecting] closing the connection with {client_addr[0]}")
            print(f"[Disconnected]\n\n")
        else:
            # print(f"[Received] {request}")
            # time.sleep(1)
            # send_data(client_socket, request)
            # file_to_binary = handle_files.file_to_binary()
            # packets = packets_list(file_to_binary[1])
            # packet_number, total_packets, acknowledged_data, window, data = request

            # if acknowledged_data == 0:
            #     # For unreliable data transfer
            #     handle_files.send_data(client_socket, ADDRESS, window = window)
            # else:
            #     # For reliable data transfer
            #     handle_files.send_data(client_socket, ADDRESS, window = window, reliable = True)
            handle_files.send_data(client, ADDRESS, request)
            print(f"sent {client}, {ADDRESS}, and {request}")
    
    client_socket.close()

quiting = False

def listening():
    while not quiting:
        print("[Listening] . . .")
        client = PC.accept()
        print(f"[Connected] new client, {client[1][0]}\n")
        handle_client(client)

threading.Thread(target=listening, daemon=True).start()
input()
quiting = True
""" import socket
import threading

HEADER = 64
PORT = 5050
# HOST = socket.gethostbyname(socket.gethostname())
HOST = "172.20.10.2"
ADDRESS = (HOST, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

intraEndpoint = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def fetch_connections():
    intraEndpoint.bind(ADDRESS)
    start_listening()


def recv_data(endpoint):
    message_length = endpoint.recv(HEADER).decode(FORMAT)

    if message_length:
        message_length = int(message_length)
        message = endpoint.recv(message_length).decode(FORMAT)

    if message == DISCONNECT_MESSAGE:
        endpoint.close()
        return "connection closed"

    return message

def send_data(endpoint, message):
    message = message.encode(FORMAT)

    message_length = len(message)
    message_length = str(message_length).encode(FORMAT)
    message_length += b' ' * (HEADER - len(message_length))

    endpoint.send(message_length)
    endpoint.send(message)

def what_to_do(endpoint, addr):
    connected = True
    while connected:
        command = str(input("What do you wanna do? "))

        if command == "send":
            message = str(input("What do you wanna send? "))
            send_data(endpoint, message)

        if command == "recv":
            received = recv_data(endpoint)
            print(received)
            send_data(endpoint, "message received!")

        if command == "end":
            connected = False
            send_data(endpoint, DISCONNECT_MESSAGE)

def start_listening():
    intraEndpoint.listen()
    print(f"[LISTENING] Host is listening on {HOST}")
    while True:
        endpoint, addr = intraEndpoint.accept()
        thread = threading.Thread(target=what_to_do, args=(endpoint, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] Host is starting...")
fetch_connections() """

# send_data(intraEndpoint, "Hello")
# message = recv_data(intraEndpoint) 

""" import socket
import threading

HEADER = 64
PORT = 5050 # The port that the server will be listening to
SERVER = socket.gethostbyname(socket.gethostname()) # The address of the host computer
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT¡"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # A new socket is created, using the IPv4 address family (socket.AF_INET)
server.bind(ADDR) # The newly created socket is bound to the address of the host computer

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) # The size of the message that will be received
        if msg_length:
            msg_length = int(msg_length) # Convert to int
            msg = conn.recv(msg_length).decode(FORMAT) # Once a connection is established, messages will be received
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr[1]}] {msg}")
            conn.send(f" message {msg} from {addr[1]} received".encode(FORMAT))

    conn.close() # The connection is closed
    

def start():
    # The function is meant to handle new connections
    server.listen()
    print(f"[LISTENING] server is listening on {SERVER}")
    while True:
        conn, addr = server.accept() # Allow the socket and address of a new connection.
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}") # Counts active threads in the process.

print("[STARTING]  server is starting...")
start() """

""" 
import socket
import time

HEADERSIZE = 10

intraEndpoint = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
intraEndpoint.bind((socket.gethostname(), 1234))
intraEndpoint.listen(5)

while True:
    extraEndpoint, address = intraEndpoint.accept()
    print(f"Connection from {address} has been established!")

    msg = "Welcome to the server!"
    msg = f'{len(msg):<{HEADERSIZE}}' + msg

    extraEndpoint.send(bytes(msg, "utf-8"))
    # extraEndpoint.close()

    while True:
        time.sleep(3)

        msg = f"The time is {time.time()}!"
        msg = f'{len(msg):<{HEADERSIZE}}' + msg

        extraEndpoint.send(bytes(msg, "utf-8"))
 """