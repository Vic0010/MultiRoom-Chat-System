import socket
import threading
import ssl

HOST = "0.0.0.0"
PORT = 5000
BUFFER_SIZE = 4096

clients = []
usernames = {}
rooms = {}
client_rooms = {}


def broadcast_room(message, room, sender):
    for client in rooms.get(room, []):
        if client != sender:
            client.send(message.encode())


def handle_client(conn, addr):

    conn.send("Enter username: ".encode())
    username = conn.recv(1024).decode()

    usernames[conn] = username
    clients.append(conn)

    print(f"[NEW USER] {username} joined from {addr}")

    while True:
        try:
            message = conn.recv(1024).decode()

            if not message:
                break

            parts = message.split(" ", 1)
            command = parts[0]

            # JOIN ROOM
            if command == "JOIN":

                room = parts[1]

                if room not in rooms:
                    rooms[room] = []

                rooms[room].append(conn)
                client_rooms[conn] = room

                conn.send(f"You joined {room}".encode())
                print(f"{username} joined room {room}")

            # ROOM MESSAGE
            elif command == "MSG":

                msg = parts[1]
                room = client_rooms.get(conn)

                if room:
                    formatted = f"[{username}@{room}] {msg}"
                    print(formatted)
                    broadcast_room(formatted, room, conn)
                else:
                    conn.send("Join a room first using JOIN".encode())

            # PRIVATE MESSAGE
            elif command == "PM":

                pm_parts = message.split(" ", 2)

                if len(pm_parts) < 3:
                    conn.send("Usage: PM username message".encode())
                    continue

                target_user = pm_parts[1]
                private_msg = pm_parts[2]

                target_conn = None

                for client, user in usernames.items():
                    if user == target_user:
                        target_conn = client
                        break

                if target_conn:
                    formatted = f"[PRIVATE {username}] {private_msg}"
                    target_conn.send(formatted.encode())
                else:
                    conn.send("User not found".encode())

            # FILE TRANSFER
            elif command == "FILE":

                file_parts = message.split(" ", 3)

                target_user = file_parts[1]
                filename = file_parts[2]
                filesize = int(file_parts[3])

                target_conn = None

                for client, user in usernames.items():
                    if user == target_user:
                        target_conn = client
                        break

                if not target_conn:
                    conn.send("User not found".encode())
                    continue

                target_conn.send(f"FILE {username} {filename} {filesize}".encode())

                received = 0

                while received < filesize:
                    data = conn.recv(BUFFER_SIZE)
                    received += len(data)
                    target_conn.send(data)

                print(f"{username} sent file {filename} to {target_user}")

        except:
            break

    print(f"[DISCONNECTED] {username}")

    room = client_rooms.get(conn)
    if room and conn in rooms[room]:
        rooms[room].remove(conn)

    clients.remove(conn)
    del usernames[conn]

    conn.close()


def start_server():

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[SECURE SERVER STARTED] Listening on port {PORT}")

    while True:

        conn, addr = server.accept()

        secure_conn = context.wrap_socket(conn, server_side=True)

        thread = threading.Thread(target=handle_client, args=(secure_conn, addr))
        thread.start()

        print(f"[ACTIVE CLIENTS] {threading.active_count()-1}")


if __name__ == "__main__":
    start_server()
