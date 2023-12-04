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
    user = input("")
    while user != KeyboardInterrupt:
        user = input("")
except KeyboardInterrupt:
    print("Exiting...")
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