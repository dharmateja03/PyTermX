import socket

# Define server host and port
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65436        # The port used by the server

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # Connect to the server
    state=1
    name=""
    name=input("Enter your name ")
    s.sendall(name.encode('utf-8'))



    while(state):
        cmd=input(">> "+name + " ~ %")

        s.sendall(cmd.encode('utf-8'))  # Send data to the server
        data = s.recv(1024)       # Receive response from the server
        print(data.decode('utf-8'))

print(f"Received from server: {data.decode()}")
