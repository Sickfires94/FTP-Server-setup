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
host = ''
BUFFER_SIZE = 1024
# binding to the host and port
sock.bind((host, port))

# Accepts up to 10 connections
sock.listen(5)
print('Socket is listening...')

while True:

    # try catch incase client terminates connection prematurely
    try:
        # Establish connection with the clients.
        con, addr = sock.accept()
        print('Connected with ', addr)

        # recieve file name and create file
        filename = con.recv(BUFFER_SIZE).decode()
        filename = "Received_" + filename
        file = open(filename, 'wb+')
        print("file name received")

        # Acknowledge that file name is received
        con.send("Ack".encode())

        # receive file
        line = con.recv(BUFFER_SIZE)
        completeData = line
        con.setblocking(False)
        print("receiving file")
        while line:
            try:
                line = con.recv(BUFFER_SIZE)
                completeData = completeData + line
            except BlockingIOError:
                break
        con.setblocking(True)

        # Acknowledge that file is received
        con.send("Ack".encode())
        print("file recieved")

        # Recieve checksum from client and generate checksum from received data
        print("Recieving and authenticating checksum")
        rec_checksum = con.recv(BUFFER_SIZE).decode()
        checksum = hashlib.md5(completeData).hexdigest()

        # write data in file and save file
        file.write(completeData)
        file.close()

        # check if received checksum and generated checksum is equal then close socket
        if checksum.strip() == rec_checksum.strip():
            con.send("File has been received successfully.".encode())
            print("File has been received successfully.")
        else:
            con.send("File has been received but is corrupted.".encode())
            print("File has been received but is corrupted.")
        try:
            con.send("Is this connected?")
        except:
            print(addr, " Disconnected")
            con.close()
    except:
        print("Connection terminated by client")

