import socket
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
start()
