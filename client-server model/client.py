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