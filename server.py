import socket
import os

def handle_client_connection(conn, storage_dir):
    """
    Handle the client connection for file upload and download.
    """
    try:
        command = conn.recv(1024).decode()

        if command.startswith('upload'):
            handle_upload(conn, command, storage_dir)
        elif command.startswith('download'):
            handle_download(conn, command, storage_dir)

    except Exception as e:
        print(f"Error: {e}")

def handle_upload(conn, command, storage_dir):
    """
    Handle file upload from the client.
    """
    _, filename = command.split()
    file_path = os.path.join(storage_dir, filename)
    file_size = int.from_bytes(conn.recv(4), 'big')

    with open(file_path, 'wb') as file:
        bytes_received = 0
        while bytes_received < file_size:
            data = conn.recv(1024)
            if not data:
                break
            file.write(data)
            bytes_received += len(data)
    print(f"Received {filename}")

def handle_download(conn, command, storage_dir):
    """
    Handle file download requests from the client.
    """
    _, filename = command.split()
    file_path = os.path.join(storage_dir, filename)
    file_size = os.path.getsize(file_path)
    conn.send(file_size.to_bytes(4, 'big'))

    with open(file_path, 'rb') as file:
        data = file.read(1024)
        while data:
            conn.send(data)
            data = file.read(1024)
    print(f"Sent {filename}")

def main():
    # Set up the server socket
    server_socket = socket.socket()
    host = '127.0.0.1'  # local host
    port = 8080
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    # Folder to store uploaded files
    storage_dir = 'server_storage'
    if not os.path.exists(storage_dir):
        os.mkdir(storage_dir)

    # Run the server to listen and process client requests
    while True:
        conn, addr = server_socket.accept()
        print(f"Got connection from {addr}")
        handle_client_connection(conn, storage_dir)
        conn.close()


main()
