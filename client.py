import socket
import threading
import ssl

SERVER_IP = "192.168.100.100"   # change to your server PC IP
PORT = 5000
BUFFER_SIZE = 4096


def receive_messages(sock):

    while True:
        try:
            data = sock.recv(BUFFER_SIZE)

            if not data:
                break

            try:
                message = data.decode()

                # FILE RECEIVING
                if message.startswith("FILE"):

                    parts = message.split(" ")

                    sender = parts[1]
                    filename = parts[2]
                    filesize = int(parts[3])

                    with open("received_" + filename, "wb") as f:

                        received = 0

                        while received < filesize:
                            chunk = sock.recv(BUFFER_SIZE)
                            f.write(chunk)
                            received += len(chunk)

                    print(f"Received file from {sender}: {filename}")

                else:
                    print(message)

            except:
                pass

        except:
            print("Disconnected from server")
            break


def start_client():

    # SSL context that ignores self-signed certificate verification
    context = ssl._create_unverified_context()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client = context.wrap_socket(sock, server_hostname=SERVER_IP)

    client.connect((SERVER_IP, PORT))

    username_prompt = client.recv(1024).decode()
    username = input(username_prompt)

    client.send(username.encode())

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.start()

    while True:

        command = input()

        # FILE SENDING
        if command.startswith("FILE"):

            parts = command.split(" ")

            if len(parts) < 3:
                print("Usage: FILE username filename")
                continue

            target = parts[1]
            filename = parts[2]

            try:
                with open(filename, "rb") as f:
                    data = f.read()

                filesize = len(data)

                header = f"FILE {target} {filename} {filesize}"

                client.send(header.encode())
                client.sendall(data)

                print("File sent")

            except:
                print("File not found")

        else:
            client.send(command.encode())


if __name__ == "__main__":
    start_client()
