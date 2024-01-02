import socket

def send_file(sock, file_path):
    """
    Read the file and sends the file size and data
    """
    with open(file_path, 'rb') as file:
        data = file.read()
        sock.send(len(data).to_bytes(4, 'big'))
        sock.send(data)

def receive_file(sock, file_path):
    """
    receive the file size and file path and writes the file
    """
    # Receive the file size
    file_size = int.from_bytes(sock.recv(4), 'big')

    # Receive and write the file
    with open(file_path, 'wb') as file:
        bytes_received = 0
        while bytes_received < file_size:
            data = sock.recv(1024)
            if not data:
                break
            file.write(data)
            bytes_received += len(data)

def main():
    # Set up the client socket
    sock = socket.socket()
    host = '127.0.0.1'  # server address
    port = 8080        # server port
    sock.connect((host, port))

    # Ask the user for the command
    command = input("Enter command (upload <filename> / download <filename>): ")
    sock.send(command.encode())

    if command.startswith('upload'):
        filename = command.split()[1]
        send_file(sock, filename)
        print(f"Uploaded {filename}")


    elif command.startswith('download'):
        filename = command.split()[1]
        receive_file(sock, filename)
        print(f"Downloaded {filename}")

    # Close the socket
    sock.close()

if __name__ == '__main__':
    main()
