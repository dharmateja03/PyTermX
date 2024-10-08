import os
import socket
import  subprocess
import shutil

# Define server host and port
HOST = '127.0.0.1'  # Localhost
PORT = 65436  # Port to listen on (non-privileged ports are > 1023)


def ls():
    """List directory contents"""
    return os.listdir()  # Equivalent to 'ls'

def cd(directory):
    """Change directory"""
    os.chdir(directory)  # Equivalent to 'cd'
    return f"Changed directory to {directory}"

def mkdir(directory):
    """Create a new directory"""
    os.mkdir(directory)  # Equivalent to 'mkdir'
    return f"Directory '{directory}' created."

def rm(file):
    """Remove a file"""
    os.remove(file)  # Equivalent to 'rm'
    return f"File '{file}' removed."

def touch(file):
    """Create an empty file"""
    with open(file, 'a'):
        os.utime(file, None)  # Equivalent to 'touch'
    return f"File '{file}' created or updated."

def mv(source, destination):
    """Move or rename a file"""
    shutil.move(source, destination)  # Equivalent to 'mv'
    return f"Moved {source} to {destination}"

def cp(source, destination):
    """Copy a file"""
    shutil.copy(source, destination)  # Equivalent to 'cp'
    return f"Copied {source} to {destination}"

def pwd():
    """Print working directory"""
    return os.getcwd()  # Equivalent to 'pwd'

def chmod(permissions, file):
    """Change file permissions"""
    os.chmod(file, int(permissions, 8))  # Equivalent to 'chmod'
    return f"Permissions for '{file}' changed to {permissions}"

def chown(owner, file):
    """Change file owner (Linux-specific)"""
    # Requires the use of os.chown, but it's limited in non-root users
    return f"Changing owner of {file} to {owner} is not available without proper privileges."

def echo(text):
    """Print a message"""
    return text  # Equivalent to 'echo'

def cat(file):
    """Print file contents"""
    with open(file, 'r') as f:
        return f.read()  # Equivalent to 'cat'

def grep(pattern, file):
    """Search for a pattern in a file"""
    with open(file, 'r') as f:
        return '\n'.join([line for line in f if pattern in line])  # Equivalent to 'grep'

def find(directory, pattern):
    """Find files matching a pattern in a directory"""
    matches = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if pattern in file:
                matches.append(os.path.join(root, file))
    return matches  # Equivalent to 'find'

def df():
    """Display disk space usage"""
    result = subprocess.run(['df', '-h'], stdout=subprocess.PIPE)  # Equivalent to 'df -h'
    return result.stdout.decode('utf-8')


# Dictionary with terminal commands as keys and the corresponding functions as values
terminal_commands = {
    "ls": ls,
    "cd": cd,
    "mkdir": mkdir,
    "rm": rm,
    "touch": touch,
    "mv": mv,
    "cp": cp,
    "pwd": pwd,
    "chmod": chmod,
    "chown": chown,
    "echo": echo,
    "cat": cat,
    "grep": grep,
    "find": find,
    "df": df
}
# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))  # Bind the socket to address and port
    s.listen()  # Enable the server to accept connections
    print(f"Server is listening on {HOST}:{PORT}")

    conn, addr = s.accept()  # Wait for a connection
    with conn:
        print(f"Connected by {addr}")
        name=conn.recv(1024).decode().strip()
        while True:
            data = conn.recv(1024)  # Receive data from the client
            client_cmd=data.decode().strip().split()
            if len(client_cmd)>1 and client_cmd[0] in terminal_commands:
                cmd=client_cmd[0]
                dir=client_cmd[1]
                msg=terminal_commands[client_cmd[0]](dir)
                conn.send(msg.encode())

            elif  client_cmd[0] in terminal_commands:
                conn.send(str(terminal_commands[client_cmd[0]]()).encode())
            else:
                conn.send((f"zsh: command not found: {client_cmd} ").encode())
            if not data:
                break
            print(f"Received from client: {data.decode()}")
            conn.sendall(b"Message received")  # Send a response to the client
