import socket

PC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = "172.20.10.2"
PORT = 3542
FORMAT = "utf-8"
HEADER = 2048
DISCONNECT = "DISCONNECT"

PC.connect((IP, PORT))
connected = True
while connected:
    message = PC.recv(HEADER).decode(FORMAT)
    if message:
        print(message)
    send = str(input("Message: "))
    if send == DISCONNECT:
        connected = False
    PC.send(send.encode(FORMAT))


""" import socket

HEADER = 64
PORT = 5050
# HOST = socket.gethostbyname(socket.gethostname())
HOST = "172.20.10.2"
ADDRESS = (HOST, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

intraEndpoint = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def recv_data(endpoint):
    message_length = endpoint.recv(HEADER).decode(FORMAT)

    if message_length:
        message_length = int(message_length)
        message = endpoint.recv(message_length).decode(FORMAT)

    if message == DISCONNECT_MESSAGE:
        endpoint.close()
        return "connection closed"

    return message

def send_data(message):
    message = message.encode(FORMAT)
    msg_length = len(message)
    msg_length = str(msg_length).encode(FORMAT)
    msg_length += b' ' * (HEADER - len(msg_length))
    intraEndpoint.send(msg_length)
    intraEndpoint.send(message)
    # recvd = intraEndpoint.recv(2048).decode(FORMAT)
    # print(recvd)

def get_connection():
    intraEndpoint.connect(ADDRESS)
    print("connected!")

get_connection()
connected = True
while connected:
    print("receiving...")
    received = recv_data(intraEndpoint)
    
    if received:
        print(received)
        send_data("message received!")

    command = str(input("What do you wanna do? "))

    if command == "send":
        message = str(input("What do you wanna send? "))
        send_data(message)

    if command == "end":
        connected = False
        send_data(DISCONNECT_MESSAGE) """

""" 
import socket

HEADER = 64
PORT = 5050 # The port that the client will be connecting to
SERVER = socket.gethostbyname(socket.gethostname()) # The address of the host computer
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT¡"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Client's socket is created
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

send(str(input("What message do you want to send: ")))
send(DISCONNECT_MESSAGE)
 """

""" import socket

HEADERSIZE = 10

intraEndpoint = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
intraEndpoint.connect((socket.gethostname(), 1234))

while True:
    full_msg = ''
    new_msg = True
    while True:
        msg = intraEndpoint.recv(16)
        if new_msg:
            print(f"new message length: {msg[:HEADERSIZE]}")
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg.decode("utf-8")

        if len(full_msg) - HEADERSIZE == msglen:
            print("full msg recvd")
            print(full_msg[HEADERSIZE:])
            new_msg = True
            full_msg = ''

print(full_msg) """