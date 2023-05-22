import socket
import hashlib

# Initialize Socket Instance
sock = ""
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created successfully.")
except:
    print("Socket could not be created")
    exit(0)

# Defining port and host
port = 6125
host = 'localhost'

BUFFER_SIZE = 1024

# Connect socket to the host and port
try:
    sock.connect((host, port))
    print('Connected to Server')
except:
    print("Could not connect to server")
    exit(0)

# input file path/name to be sent
file_path = input("input file path: ")
filename = file_path.split("\\")[-1]
file = ""
try:
    file = open(file_path, 'rb')
except FileNotFoundError:
    print("File not found")
    exit(0)

# send file name and wait for Acknowledgment
sock.send(filename.encode())

if sock.recv(BUFFER_SIZE).decode() != "Ack":
    print("Ack not recieved")
print("File name sent")


# send data to the client and wait for Acknowledgement
line = file.read()
sock.sendall(line)

if sock.recv(BUFFER_SIZE).decode() != "Ack":
    print("Ack not recieved")
print("File recieved by host")


# calculate checksum and send it to server
checksum = hashlib.md5(line).hexdigest()
sock.send(checksum.encode())

file.close()


# wait for server to send file receive status
sock.setblocking(False)
response = ""
while not response:
    try:
        response = sock.recv(BUFFER_SIZE).decode()
    except:
        pass
print(response)

# close socket
sock.close()
print("Connection Closed.")

