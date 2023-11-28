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
ADDRESSES = []
HEADER = 64

def dns_server():
    dns_endpoint = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket
    dns_endpoint.connect(DNS_ADDRESS) # Connect to the DNS server

    # Get the list of addresses of hosts that have already connected
    message_length = dns_endpoint.recv(HEADER).decode(FORMAT)
    if message_length:
        addresses = dns_endpoint.recv(int(message_length))
        ADDRESSES = pickle.loads(addresses)
        print(f"Addresses: {ADDRESSES}")

    recv_thread = threading.Thread(target=lambda: dns_addresses(dns_endpoint))
    recv_thread.start()
    # dns_socket.listen() # Listen for new connections

    # while True:
    #     endpoint, address = dns_socket.accept() # Accept a connection        
    #     message = pickle.dumps(HOSTS) # Pickle the list to send it to the new connection

    #     # Calculate the message's length
    #     msg_length = len(message) 
    #     msg_length = str(msg_length).encode(FORMAT)
    #     msg_length += b' ' * (HEADER - len(msg_length))
        
    #     endpoint.send(msg_length) # Send the new user the length of the message
    #     endpoint.send(message) # Send the new user the list of all hosts connected

    #     HOSTS.append(address) # Add the new host to the list of hosts
    #     new_thread = threading.Thread(target=handle_host, args=(endpoint, address))
    #     new_thread.start()

def handle_host(endpoint, address):
    # Receive new messages from DNS
    # new_thread = threading.Thread(target=dns_data, arg=endpoint)
    # new_thread.start()
    pass

def send_data(endpoint):
    pass

def dns_addresses(endpoint):
    connected = True
    while connected:
        # print("Connected and ready to receive addresses . . . ")
        msg_length = endpoint.recv(HEADER).decode(FORMAT) # The size of the message that will be received
        if msg_length:
            message = endpoint.recv(int(msg_length)) # Once a connection is established, messages will be received
            address = pickle.loads(message)
            ADDRESSES.append(address)
            print(f"Addresses: {ADDRESSES} {type(address)}")

    endpoint.close() # The connection is closed

# lists = [("socket", ("192.168.48.5", 5050))]
# conn, addr = lists[0]
# print(f"lists[0]: {lists[0]}")
# print(f"socket: {conn}")
# print(f"addr: {addr}")
# print(f"IP: {addr[0]}")
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
