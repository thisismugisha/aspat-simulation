import socket
import threading
import pickle

def wlan_ip():
    """ 
    Creates a dummy socket to retrieve the wireless LAN IP address.

        Returns: 
            IP (string): A String containing the WLAN IP address

    """

    dummy_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create a dummy socket
    try:
        dummy_IP = '10.255.255.255'
        dummy_port = 1
        
        dummy_socket.connect((dummy_IP, dummy_port)) # Connect to dummy socket; doesn't even have to be reachable
        IP = dummy_socket.getsockname()[0]
    except:
        IP = '127.0.0.1' # Reject the localhost IP
    finally:
        dummy_socket.close() # Close the dummy socket
    return IP

PORT = 5050
DNS = "172.20.10.2" # The DNS IP address that everyone connects to to know who's on the network
IP = wlan_ip()
ADDRESS = (IP, PORT)
DNS_ADDRESS = (DNS, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
HOSTS = []
SOCKETS = []
HEADER = 64

def dns_server():
    print("Creating a socket . . . ")
    dns_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a DNS socket
    print("binding the address . . . ")
    dns_socket.bind(DNS_ADDRESS) # Bind the DNS socket
    print("Listening . . . ")
    dns_socket.listen() # Listen for new connections

    while True:
        new_host = dns_socket.accept() # Accept a connection
        new_endpoint, new_address = new_host
        print(f"Accepted a connection from {new_address}")
        existing_addresses = [] # Create a temporary list of hosts' existing addresses

        if HOSTS: # If there are any hosts connected
            for HOST in HOSTS:
                existing_addresses.append(HOST[1]) # Add each address in the HOSTS list to the temporary list of hosts' existing addresses
                existing_endpoint = HOST[0] # Get the host socket. The new variable was created to make the code more readable

                message = pickle.dumps(new_address) # Pickle the address of new connection to send it to the other hosts    

                # Calculate the message's length
                msg_length = len(message)
                msg_length = str(msg_length).encode(FORMAT)
                msg_length += b' ' * (HEADER - len(msg_length))

                existing_endpoint.send(msg_length) # Send each host the length of the message
                existing_endpoint.send(message) # Send the address of the newly connected host to the rest of the hosts, one by one

        HOSTS.append(new_host)        
        message = pickle.dumps(existing_addresses) # Pickle the list to send it to the new connection

        # Calculate the message's length
        msg_length = len(message) 
        msg_length = str(msg_length).encode(FORMAT)
        msg_length += b' ' * (HEADER - len(msg_length))
        
        new_endpoint.send(msg_length) # Send the new user the length of the message
        new_endpoint.send(message) # Send the new user the list of all hosts connected

        """ message = address # Store the address of new connection to send it to the other hosts

        # Calculate the message's length
        msg_length = len(message) 
        msg_length = str(msg_length).encode(FORMAT)
        msg_length += b' ' * (HEADER - len(msg_length))

        if not SOCKETS: # Checks if the list is empty
            continue

        else:
            for ENDPOINT in ENDPOINTS:
                ENDPOINT.send(msg_length)
                ENDPOINT.send(message) # Send the address of the newly connected host to the rest of the hosts, one by one

        HOSTS.append(address) # Add the new host to the list of hosts
        ENDPOINTS.append(endpoint) # Add the new endpoint to the list of endpoints
        new_thread = threading.Thread(target=handle_host, args=(endpoint, address))
        new_thread.start() """

def handle_host(endpoint, address):
    pass

def send_data(endpoint):
    pass

def dns_data(endpoint):
    connected = True
    while connected:
        msg_length = endpoint.recv(HEADER).decode(FORMAT) # The size of the message that will be received
        if msg_length:
            msg_length = int(msg_length) # Convert to int
            message = endpoint.recv(msg_length).decode(FORMAT) # Once a connection is established, messages will be received

            if message == DISCONNECT_MESSAGE:
                connected = False

            if type(message) == list:
                HOSTS = message

            # print(f"[{addr[1]}] {message}")
            # endpoint.send(f" message {message} from {addr[1]} received".encode(FORMAT))

    endpoint.close() # The connection is closed

dns_server()
    
# HEADER = 64
""" IP = wlan_ip()
PORT = 5050
ADDRESS = (IP, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
DNS_IP = [IP]

my_endpoint = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def handle_endpoint(endpoint):
    pass

def fetch_connections():
    my_endpoint.bind(ADDRESS)
    my_endpoint.listen()

    while True:
        new_endpoint = my_endpoint.accept()[0]
        new_endpoint_thread = threading.Thread(target=handle_endpoint, arg=(new_endpoint))
        new_endpoint_thread.start()

def get_connections():
    my_endpoint.connect(ADDRESS)

def start():
    fetch_connections_thread = threading.Thread(target=fetch_connections)
    get_connections_thread = threading.Thread(target=get_connections)

    fetch_connections_thread.start()
    get_connections_thread.start() """
